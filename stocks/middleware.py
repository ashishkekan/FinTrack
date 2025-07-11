from django.urls import reverse


class SidebarMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define navigation links with name, URL, icon, and styling
        nav_links = [
            {
                "name": "Dashboard",
                "url_name": "home",
                "icon": "fa-home",
                "font_semibold": True,
            },
            {"name": "Portfolio", "url_name": "transactions-list", "icon": "fa-chart-line"},
            {
                "name": "Transactions",
                "url_name": "transactions-list",
                "icon": "fa-exchange-alt",
            },
            {
                "name": "Calculator",
                "url_name": "avg_price_calculator",
                "icon": "fa-calculator",
            },
        ]
        # Add admin link for staff users
        if request.user.is_authenticated and request.user.is_staff:
            nav_links.append(
                {"name": "Admin", "url_name": "admin:index", "icon": "fa-cog"}
            )

        # Add authentication links
        if request.user.is_authenticated:
            nav_links.append(
                {"name": "Logout", "url_name": "logout", "icon": "fa-sign-out-alt"}
            )
        else:
            nav_links.append(
                {"name": "Login", "url_name": "login", "icon": "fa-sign-in-alt"}
            )
            nav_links.append(
                {"name": "Sign Up", "url_name": "signup", "icon": "fa-user-plus"}
            )

        # Add URL and active state
        current_url_name = (
            request.resolver_match.url_name if request.resolver_match else None
        )
        for link in nav_links:
            link["url"] = reverse(link["url_name"])
            link["is_active"] = link["url_name"] == current_url_name

        # Inject context
        request.sidebar_nav_links = nav_links
        request.sidebar_user = (
            {
                "name": request.user.get_full_name() or request.user.username,  # Use get_full_name() or fallback to username
                "is_staff": request.user.is_staff,
            }
            if request.user.is_authenticated
            else None
        )

        response = self.get_response(request)
        return response
