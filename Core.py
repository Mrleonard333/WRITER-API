# source /c/Users/MrLeonard/Documents/VS_PROJECTS/Python_Projects/Writer-API/venv/Scripts/activate

from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__) # v Will configure the database connection
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://_User_:_Password_@_host_:3306/_Schema_"

app.app_context().push() # < To avoid configuration errors
app.config["JWT_SECRET_KEY"] = "_SCECRET_KEY_"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config["JWT_ALGORITHM"] = "_Algorithm_"

app.config["JWT_TOKEN_LOCATION"] = "headers"
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"

JWT = JWTManager(app)
DataBase = SQLAlchemy(app)

class code(DataBase.Model): # < Will get be a model of a database table
    id = DataBase.Column(DataBase.Integer, primary_key=True)
    code = DataBase.Column(DataBase.String(650))
    description = DataBase.Column(DataBase.String(255))

    def Format_Data(self): # < It will show the data in form of dict
        return {"id":self.id, "code":self.code, "description":self.description}

class creators(DataBase.Model):
    id = DataBase.Column(DataBase.Integer, primary_key=True)
    username = DataBase.Column(DataBase.String(50))
    password = DataBase.Column(DataBase.String(50))

    def Format_Data(self):
        return {"id":self.id, "username":self.username, "password":self.password}

@app.route("/get_code", methods=["POST"])
def GET():
    Codes = dict()
    Description = str(request.json["description"]) # < Will request json data from user

                        # v Will get the code table data
    for DB_Code in code.query.all():
        DB_Code = DB_Code.Format_Data() # < Will format the data in a dict

        if DB_Code["description"] == Description:
                        # v Will return the dict in jason format
            return jsonify({"Results":DB_Code}), 200 # < Server Status
        else:
            Counter = 0
            for Code_Tags in DB_Code["description"].split():
                if Code_Tags in Description:
                    Counter += 1
                    if not Codes:
                        Codes.update({"Infos":[DB_Code], "Tags_Count":[Counter]})
                    else: 
                        Codes["Infos"].append(DB_Code)
                        Codes["Tags_Count"].append(Counter)
    More_Counts = 0
    Position = 0

    try:
        for Count in Codes["Tags_Count"]: # < Will filter the result [The one with more counts]
            if Count >= More_Counts:
                More_Counts = Count
                Info = Codes["Infos"][Position]
            Position += 1
        
            return jsonify({"Results":Info}), 200
    except:
        return jsonify({"ERROR":"Nothing about was found"}), 404

@app.route("/store_code", methods=["POST"])
@jwt_required() # < JWT Token will be required to access the content
def STORE():
    get_jwt_identity() # < Will verify the user's Token

    Id = 0
    Cadastrated = False
    Code = request.json["code"].replace("'", "\'")
    User = request.json["user"].replace("'", "\'")
    Pass = request.json["pass"].replace("'", "\'")
    Desciption = request.json["description"].replace("'", "\'")

    for creator in creators.query.all():
        creator = creator.Format_Data()

        if User.lower() == creator["username"].lower() and  Pass.lower() == creator["password"].lower():
            Cadastrated = True
            break
    
    if not Cadastrated:
        return jsonify({"ERROR":"Creator not found"}), 404

    for DB_Code in code.query.all():
        DB_Code = DB_Code.Format_Data()
        Id = DB_Code["id"]

        if Code.lower() == DB_Code["code"].lower():
            return jsonify({"ERROR":"Code already exists"}), 409

    Id += 1
    DataBase.session.add(code(id=Id, code=Code, description=Desciption)) # < Will add the new data to the DataBase
    DataBase.session.commit() # < Will save the changes

    return jsonify({"Result":"Code sended"}), 200

app.run(debug=True) # < Will reload the system if it has changed
