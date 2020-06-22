from forecastapp import create_app, db
from forecastapp.models import User, Post
from forecastapp.database.models import MergedPdcn, WholesalerFamily

app = create_app()
ctx = app.app_context()
ctx.push()
db.create_all()
ctx.pop()

print("----DB created/modified.----")
