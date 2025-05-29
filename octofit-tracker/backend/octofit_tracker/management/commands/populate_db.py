from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from octofit_tracker.test_data import test_data

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Populate users
        users = [User(**user_data) for user_data in test_data['users']]
        User.objects.bulk_create(users)

        # Map usernames to user instances
        user_map = {user.username: user for user in User.objects.all()}

        # Verify user_map population
        if len(user_map) != len(test_data['users']):
            self.stdout.write(f"Warning: user_map contains {len(user_map)} entries, but test_data['users'] contains {len(test_data['users'])} entries.")

        # Enhanced logging for missing usernames
        missing_usernames = [username for team_data in test_data['teams'] for username in team_data.get('members', []) if username not in user_map]
        if missing_usernames:
            self.stdout.write(f"Error: The following usernames are missing from user_map: {missing_usernames}")

        # Log user_map contents
        self.stdout.write(f"user_map: {user_map}")

        # Populate teams with individual save calls
        for team_data in test_data['teams']:
            self.stdout.write(f"Processing team: {team_data}")
            missing_members = [username for username in team_data.get('members', []) if username not in user_map]
            if missing_members:
                self.stdout.write(f"Error: Missing members for team '{team_data['name']}': {missing_members}")
                continue

            try:
                team_data['members'] = [user_map[username] for username in team_data['members']]
                team = Team(**team_data)
                team.save()  # Save each team individually
            except Exception as e:
                self.stdout.write(f"Unexpected error while processing team '{team_data['name']}': {e}")
                self.stdout.write(f"Exception details: {e.__class__.__name__}: {e}")

        # Populate activities
        activities = []
        for activity_data in test_data['activities']:
            try:
                activity_data['user'] = user_map[activity_data['user']]  # Map user to User instance
                activities.append(Activity(**activity_data))
            except KeyError as e:
                self.stdout.write(f"Error: Username {e} not found in user_map for activity {activity_data}")
            except Exception as e:
                self.stdout.write(f"Unexpected error while processing activity {activity_data}: {e}")
        Activity.objects.bulk_create(activities)

        # Fix Leaderboard model population
        leaderboard_entries = []
        for entry_data in test_data['leaderboard']:
            try:
                entry_data['user'] = user_map[entry_data['user']]  # Map user to User instance
                leaderboard_entries.append(Leaderboard(**entry_data))
            except KeyError as e:
                self.stdout.write(f"Error: Username {e} not found in user_map for leaderboard entry {entry_data}")
            except Exception as e:
                self.stdout.write(f"Unexpected error while processing leaderboard entry {entry_data}: {e}")
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Fix Team model population
        for team_data in test_data['teams']:
            self.stdout.write(f"Processing team: {team_data}")
            missing_members = [username for username in team_data.get('members', []) if username not in user_map]
            if missing_members:
                self.stdout.write(f"Error: Missing members for team '{team_data['name']}': {missing_members}")
                continue

            try:
                team_data['members'] = [user_map[username] for username in team_data['members']]
                team = Team(**team_data)
                team.save()  # Save each team individually
            except Exception as e:
                self.stdout.write(f"Unexpected error while processing team '{team_data['name']}': {e}")
                self.stdout.write(f"Exception details: {e.__class__.__name__}: {e}")

        # Populate workouts
        workouts = [Workout(**workout_data) for workout_data in test_data['workouts']]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))