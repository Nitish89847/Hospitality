from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from insurance.models import Policy
from hospitals.models import Hospital, RoomType
from hospitals.services.eligibility_engine import compute_room_coverage

User = get_user_model()


class EligibilityEngineTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass1234")

        self.hospital = Hospital.objects.create(
            name="Test Hospital",
            city="Bangalore",
            specialties=["cardiology"],
            empanelled_schemes=["PM-JAY"],
            network_insurers=["Star Health"],
            ownership_type="private",
        )

        self.policy = Policy.objects.create(
            insurer="Star Health",
            scheme_type="private",
            sum_insured=Decimal("500000"),
            room_eligibility={
                "category": "semi_private",
                "cap_per_day": 3000,
                "icu_covered": True,
                "icu_cap_per_day": 8000,
            },
            co_pay_percent=Decimal("10"),
            owner=self.user,
        )

    def make_room(self, category, cost):
        return RoomType.objects.create(
            hospital=self.hospital,
            category=category,
            indicative_cost_per_day=Decimal(str(cost)),
        )

    def test_general_ward_covered_with_co_pay(self):
        room = self.make_room("general_ward", 1200)
        result = compute_room_coverage(self.policy, room)
        self.assertTrue(result["covered"])
        self.assertEqual(result["estimated_out_of_pocket_per_day"], 120.0)

    def test_semi_private_covered_at_exact_tier(self):
        room = self.make_room("semi_private", 2800)
        result = compute_room_coverage(self.policy, room)
        self.assertTrue(result["covered"])
        self.assertEqual(result["estimated_out_of_pocket_per_day"], 280.0)

    def test_private_room_exceeds_policy_tier(self):
        room = self.make_room("private", 5500)
        result = compute_room_coverage(self.policy, room)
        self.assertFalse(result["covered"])
        self.assertEqual(result["estimated_out_of_pocket_per_day"], 5500.0)

    def test_semi_private_over_daily_cap_charges_excess_plus_co_pay(self):
        # Cap is 3000/day; this room costs more than the cap despite being the right tier
        room = self.make_room("semi_private", 3500)
        result = compute_room_coverage(self.policy, room)
        self.assertTrue(result["covered"])
        # cap_excess = 500, co_pay = 3000*10% = 300 -> total 800
        self.assertEqual(result["estimated_out_of_pocket_per_day"], 800.0)

    def test_icu_within_cap_applies_co_pay_only(self):
        room = self.make_room("icu", 7000)
        result = compute_room_coverage(self.policy, room)
        self.assertTrue(result["covered"])
        # no cap excess (7000 < 8000), co_pay = 7000*10% = 700
        self.assertEqual(result["estimated_out_of_pocket_per_day"], 700.0)

    def test_icu_over_cap_charges_excess_plus_co_pay(self):
        room = self.make_room("icu", 9500)
        result = compute_room_coverage(self.policy, room)
        self.assertTrue(result["covered"])
        # cap_excess = 1500, co_pay on covered portion (8000) = 800 -> total 2300
        self.assertEqual(result["estimated_out_of_pocket_per_day"], 2300.0)

    def test_icu_not_covered_when_policy_excludes_it(self):
        self.policy.room_eligibility["icu_covered"] = False
        self.policy.save()
        room = self.make_room("icu", 9500)
        result = compute_room_coverage(self.policy, room)
        self.assertFalse(result["covered"])
        self.assertEqual(result["estimated_out_of_pocket_per_day"], 9500.0)

    def test_icu_uncapped_when_no_cap_specified(self):
        self.policy.room_eligibility["icu_cap_per_day"] = None
        self.policy.save()
        room = self.make_room("icu", 9500)
        result = compute_room_coverage(self.policy, room)
        self.assertTrue(result["covered"])
        # no cap excess, co_pay on full amount = 950
        self.assertEqual(result["estimated_out_of_pocket_per_day"], 950.0)