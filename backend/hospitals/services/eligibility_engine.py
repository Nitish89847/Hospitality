ROOM_CATEGORY_RANK = {
    "general_ward": 1,
    "semi_private": 2,
    "private": 3,
    "deluxe": 4,
    "suite": 5,
}

ICU_CATEGORIES = {"icu", "icu_hdu", "nicu", "picu", "ccu"}


def apply_co_pay(policy, covered_amount):
    co_pay_percent = float(policy.co_pay_percent or 0)
    return covered_amount * (co_pay_percent / 100)


def compute_regular_room_coverage(policy, room_type):
    room_eligibility = policy.room_eligibility
    policy_category = room_eligibility.get("category")
    cap_per_day = room_eligibility.get("cap_per_day", 0)

    policy_rank = ROOM_CATEGORY_RANK.get(policy_category, 0)
    room_rank = ROOM_CATEGORY_RANK.get(room_type.category, 0)
    daily_cost = float(room_type.indicative_cost_per_day)

    if room_rank > policy_rank:
        return {
            "covered": False,
            "reason": f"Policy covers up to '{policy_category}'; this room exceeds that tier.",
            "estimated_out_of_pocket_per_day": round(daily_cost, 2),
        }

    cap_excess = max(0, daily_cost - cap_per_day)
    covered_portion = min(daily_cost, cap_per_day)
    co_pay_amount = apply_co_pay(policy, covered_portion)
    total_out_of_pocket = cap_excess + co_pay_amount

    return {
        "covered": True,
        "reason": f"Within your policy's room eligibility (co-pay: {policy.co_pay_percent}%).",
        "estimated_out_of_pocket_per_day": round(total_out_of_pocket, 2),
    }


def compute_icu_coverage(policy, room_type):
    room_eligibility = policy.room_eligibility
    icu_covered = room_eligibility.get("icu_covered", True)
    icu_cap = room_eligibility.get("icu_cap_per_day")
    daily_cost = float(room_type.indicative_cost_per_day)

    if not icu_covered:
        return {
            "covered": False,
            "reason": "Your policy does not cover ICU/critical care stays.",
            "estimated_out_of_pocket_per_day": round(daily_cost, 2),
        }

    if icu_cap is None:
        covered_portion = daily_cost
        cap_excess = 0
    else:
        cap_excess = max(0, daily_cost - icu_cap)
        covered_portion = min(daily_cost, icu_cap)

    co_pay_amount = apply_co_pay(policy, covered_portion)
    total_out_of_pocket = cap_excess + co_pay_amount

    return {
        "covered": True,
        "reason": f"ICU covered{' up to ₹' + str(icu_cap) + '/day' if icu_cap else ''} (co-pay: {policy.co_pay_percent}%).",
        "estimated_out_of_pocket_per_day": round(total_out_of_pocket, 2),
    }


def compute_room_coverage(policy, room_type):
    if room_type.category in ICU_CATEGORIES:
        return compute_icu_coverage(policy, room_type)
    return compute_regular_room_coverage(policy, room_type)