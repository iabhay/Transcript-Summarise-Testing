from users.users_helper import UsersHelper
from users.premium_user.premium_user_controller import PremiumUserController
from users.admin.admincontroller import AdminController
from users.submittedvideo.video_service import VideoService


class NonPremiumMap:
    def __init__(self, uid):
        self.user_helper = UsersHelper(uid)
        self.video_service = VideoService(uid)

    def non_premium_menu(self):
        non_premium_dict = {
            1: self.video_service.submit_video,
            2: self.user_helper.upgrade_to_premium
        }
        return non_premium_dict


class PremiumMap:
    def __init__(self, uid):
        self.user_helper = UsersHelper(uid)
        self.premium_controller = PremiumUserController(uid)
        self.video_service = VideoService(uid)

    def premium_menu(self):
        premium_dict = {
            1: self.video_service.submit_video,
            2: self.premium_controller.send_message_to_admin,
            3: self.premium_controller.premium_listing_of_banned_url,
            4: self.premium_controller.view_my_history,
            5: self.premium_controller.view_my_premium_listing,
            6: self.user_helper.downgrade_to_basic
        }
        return premium_dict


class AdminMap:
    def __init__(self, uid):
        self.uid = uid
        self.adm = AdminController(self.uid)

    def admin_menu(self):
        admin_dict = {
            1: self.adm.view_user,
            2: self.adm.view_all_users,
            3: self.adm.downgrade_premium_user,
            4: self.adm.ban_user,
            5: self.adm.unban_user,
            6: self.adm.ban_url,
            7: self.adm.unban_url,
            8: self.adm.unban_url_for_premium_user,
            10: self.adm.view_history_of_user,
            11: self.adm.view_all_history,
            12: self.adm.view_premium_listing_of_user,
            13: self.adm.view_all_premium_listings,
            14: self.adm.show_all_ban_urls,
            15: self.adm.show_ban_url
        }
        return admin_dict

    def message_menu(self):
        message_views = {
            1: self.adm.messages_from_premium_users,
            2: self.adm.messages_from_non_premium_users,
            3: self.adm.message_from_user,
            4: self.adm.view_all_messages
        }
        return message_views
