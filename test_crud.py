# test_crud.py

from db.database import SessionLocal
from db.crud import (
    create_user_with_profile,
    get_user_profile,
    get_user_by_email,
    save_trip_history,
    get_user_trips,
    user_exists
)

# Create session
db = SessionLocal()

print("=" * 60)
print("Testing CRUD Operations for GlobeGenie")
print("=" * 60)

# Test 1: Check if user exists
print("\n1. Checking if user exists...")
email = "test@example.com"
if user_exists(db, email):
    print(f"⚠️  User {email} already exists. Skipping creation.")
    user = get_user_by_email(db, email)
else:
    # Test 2: Create user with profile
    print(f"\n2. Creating new user: {email}")
    user, profile = create_user_with_profile(
        db,
        email=email,
        name="Test User",
        home_city="San Francisco",
        travel_style="adventure",
        budget_range="medium",
        pace_preference="moderate",
        interests=["hiking", "culture", "food", "photography"]
    )
    print(f"✅ Created user ID: {user.id}")
    print(f"✅ Created profile ID: {profile.id}")

# Test 3: Retrieve and display profile
print(f"\n3. Retrieving profile for user ID: {user.id}")
profile = get_user_profile(db, user.id)
if profile:
    print(f"✅ User: {user.name}")
    print(f"✅ Email: {user.email}")
    print(f"✅ Home City: {user.home_city}")
    print(f"✅ Travel Style: {profile.travel_style}")
    print(f"✅ Budget Range: {profile.budget_range}")
    print(f"✅ Pace Preference: {profile.pace_preference}")
    print(f"✅ Interests: {', '.join(profile.interests)}")
else:
    print("❌ Profile not found!")

# Test 4: Save a trip
print(f"\n4. Saving trip history...")
trip = save_trip_history(
    db,
    user_id=user.id,
    destination="Bali, Indonesia",
    trip_dates={"start": "2025-06-01", "end": "2025-06-07"},
    duration_days=7,
    num_travelers=2,
    budget_target=3000.0,
    total_cost=2850.0,
    trip_data={"sample": "itinerary data"},
    activity_summary="Beach activities, temple visits, cultural experiences",
    destination_info={"climate": "tropical", "currency": "IDR"}
)
print(f"✅ Saved trip ID: {trip.id}")
print(f"✅ Destination: {trip.destination}")
print(f"✅ Budget: ${trip.budget_target} | Actual: ${trip.total_cost}")
print(f"✅ Within Budget: {trip.within_budget}")

# Test 5: Retrieve user trips
print(f"\n5. Retrieving all trips for user...")
trips = get_user_trips(db, user.id)
print(f"✅ Found {len(trips)} trip(s):")
for t in trips:
    print(f"   → Trip #{t.id}: {t.destination} (${t.total_cost})")

# Close session
db.close()

print("\n" + "=" * 60)
print("✅ All CRUD operations completed successfully!")
print("=" * 60)