import json

from insider.webapp.models import LinkedInUserData, LinkedInConnection
from linkedin.models import AccessToken
from linkedin import linkedin
from insider.webapp.views.home import LinkedInMixin


def refresh_linkedin_data():
    """Refresh all of the current LinkedIn data for users."""
    limn = LinkedInMixin()
    limn.set_up_linkedin()

    for ud in LinkedInUserData.objects.all():
        limn.authentication.token = AccessToken(ud.access_token, ud.expires_in)
        
        try:
            conn = limn.application.get_connections(selectors=limn.get_shared_profile_fields())
            ud.connections_json = json.dumps(conn)
        except Exception as e:
            print 'Exception getting connections with response'

        try:
            prof = limn.application.get_profile(selectors=limn.get_personal_profile_fields())
            ud.profile_json = json.dumps(prof)
        except Exception as e:
            print 'Exception getting profile with response'

        ud.save()


def populate_user_data():
    for ud in LinkedInUserData.objects.all():
        if ud.profile_json:
            linkedin_profile = json.loads(ud.profile_json)

            ud.first_name = linkedin_profile.get('firstName', '')
            ud.last_name = linkedin_profile.get('lastName', '')
            ud.headline = linkedin_profile.get('headline', '')
            ud.picture_url = linkedin_profile.get('pictureUrl', '')
            ud.email = linkedin_profile.get('emailAddress', '')
            ud.location = linkedin_profile.get('location', {}).get('name', '')
            
            positions = linkedin_profile.get('positions', {}).get('values', [])
            if len(positions) > 0:
                ud.position_title = positions[0].get('title', '')
                ud.position_company = positions[0].get('company', {}).get('name', '')
                ud.position_industry = positions[0].get('company', {}).get('industry', '')

            ud.public_profile_url = linkedin_profile.get('publicProfileUrl', '')

            ud.save()


def populate_connections():
    for ud in LinkedInUserData.objects.all():
        if ud.connections_json:
            connections = json.loads(ud.connections_json).get('values', [])
            if len(connections) > 0:
                # Clear current connections.
                ud.linkedinconnection_set.all().delete()

                for c in connections:
                    conn = LinkedInConnection()

                    conn.connected_with = ud
                    conn.user_id = c.get('id', '')
                    conn.first_name = c.get('firstName', '')
                    conn.last_name = c.get('lastName', '')
                    conn.headline = c.get('headline', '')
                    conn.picture_url = c.get('pictureUrl', '')
                    conn.location = c.get('location', {}).get('name', '')

                    positions = c.get('positions', {}).get('values', [])
                    if len(positions) > 0:
                        conn.position_title = positions[0].get('title', '')
                        conn.position_company = positions[0].get('company', {}).get('name', '')
                        conn.position_industry = positions[0].get('company', {}).get('industry', '')

                    conn.public_profile_url = c.get('publicProfileUrl', '')
                    conn.full_connection_json = json.dumps(c)

                    conn.save()
