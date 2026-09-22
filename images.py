from urllib.parse import quote


def white_url(url):
    url = (url or "").strip()
    if not url:
        return "https://images.weserv.nl/?url=images.unsplash.com/photo-1505740420928-5e560c06d30e&bg=ffffff&fit=contain&w=900&h=900"
    if "weserv.nl" in url and "bg=" in url:
        return url
    raw = url.replace("https://", "").replace("http://", "")
    return (
        "https://images.weserv.nl/?url="
        + quote(raw, safe="")
        + "&bg=ffffff&fit=contain&w=900&h=900&il"
    )


def install_images(app):
    if getattr(app, "_images", False):
        return
    app._images = True

    @app.template_filter("whitebg")
    def whitebg(url):
        return white_url(url)
