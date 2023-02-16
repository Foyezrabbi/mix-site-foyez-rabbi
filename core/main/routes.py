"""
Main page routes.
"""

import os
from urllib.parse import urlparse
from ..rapid.api import get_email
from ..rapid.coin import get_price

from flask import (
    render_template, url_for, abort, flash, redirect,
    request, current_app, make_response, send_from_directory, Response
)

from .. import db
from . import main
from .models import Project

from ..email import send_email
from ..contact.models import Contact
from ..contact.forms import ContactForm


@main.route("/", methods=['GET', 'POST'], strict_slashes=False)
def homePage():
    page_title = 'Hello, i am Foyez Rabbi'

    form = ContactForm()
    if form.validate_on_submit():
        try:
            contact = Contact(
                fullname=form.fullname.data,
                email=form.email.data.lower(),
                phone=form.phone.data,
                subject=form.subject.data,
                message=form.message.data
            )
            db.session.add(contact)
            db.session.commit()
            msg = f"""
                Hey {form.fullname.data},
                your message has been sent successfully.
                We will contact you shortly.
            """
            flash(msg, "success")
            return redirect(request.url)
        except Exception as e:
            abort(400)

    return render_template(  # FoyezRabbi
        'index.html',
        form=form,
        page_title=page_title
    )


@main.route("/at-services/", strict_slashes=False)
def servicePage():
    page_title = 'at-your-service'
    return render_template(
        'page/service.html',
        page_title=page_title
    )


@main.route("/sitemap/", strict_slashes=False)
@main.route("/sitemap.xml/", strict_slashes=False)
def sitemap():
    host_components = urlparse(request.host_url)
    host_base = host_components.scheme + "://" + host_components.netloc

    static_urls = list()
    for rule in current_app.url_map.iter_rules():
        if (
            not str(rule).startswith("/21fh08/"),
            not str(rule).startswith("/errors/")
        ):
            if "GET" in rule.methods and len(rule.arguments) == 0:
                url = {
                    "loc": f"{host_base}{str(rule)}",
                    "changefreq": "weekly",
                    "priority": "0.9"
                }
                static_urls.append(url)

    xml_sitemap = render_template(
        "sitemap.xml",
        static_urls=static_urls,
        host_base=host_base
    )
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"

    return response


@main.route('/robots.txt/', strict_slashes=False)
def noindex():
    Disallow = lambda string: f'Disallow: {string}'
    r = Response(
        "User-Agent: *\n{0}\n".format("\n".join([Disallow('/21fh08/')])),
        status=200, mimetype="text/plain"
    )
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return r


@main.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(current_app.root_path, 'static'),
        'img/favicon.ico'
    )


@main.route("/get-email/<url>")
def email(url):
    return get_email(url)


@main.route("/get-price/<url>")
def coin(url):
    return get_price(url)
