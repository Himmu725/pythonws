from db_connection import get_db

def read_profile(file_path):
    profile_data = {}
    with open(file_path, "r") as f:
        for line in f:
            key, value = line.strip().split(":", 1)
            profile_data[key.strip()] = value.strip()
    return profile_data

def setup_profile():
    db = get_db()
    profile = read_profile("profile.txt")
    db.profile.delete_many({})
    db.profile.insert_one(profile)
    print("✅ Profile inserted into MongoDB.")

if __name__ == "__main__":
    setup_profile()
