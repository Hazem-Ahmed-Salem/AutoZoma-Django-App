def user_directory_path(instance , filename):
    return f'user_{instance.seller.user.id}/Listings/{filename}'