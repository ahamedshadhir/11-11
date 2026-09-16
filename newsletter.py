from flask import flash, redirect, request, url_for

def install_newsletter(app):
    if getattr(app, '_newsletter', False):
        return
    app._newsletter = True

    @app.route('/newsletter', methods=['POST'])
    def newsletter():
        email = (request.form.get('email') or '').strip()
        if email:
            flash('Thanks, we will send offers to %s.' % email, 'success')
        return redirect(request.referrer or url_for('index'))
