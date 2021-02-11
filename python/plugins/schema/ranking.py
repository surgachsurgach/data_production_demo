guest_house_ranking_weekly = {
    "task_name": "guest_house_ranking_weekly",
    "class": "com.yelp.batch.mart.guestHouse.app.GuestHouseRankingWeekly"
}

guest_house_ranking_monthly = {
    "task_name": "guest_house_ranking_monthly",
    "class": "com.yelp.batch.mart.guestHouse.app.GuestHouseRankingMonthly"
}

guest_house_ranking_yearly = {
    "task_name": "guest_house_ranking_yearly",
    "class": "com.yelp.batch.mart.guestHouse.app.GuestHouseRankingYearly"
}

guest_house_ranking_delivery = {
    "task_name": "guest_house_ranking_delivery",
    "class": "com.yelp.batch.mart.guestHouse.app.BuildGuestHouseRankingDelivery"
}

TABLES = [
    guest_house_ranking_weekly,
    guest_house_ranking_monthly,
    guest_house_ranking_yearly,
    guest_house_ranking_delivery,
]