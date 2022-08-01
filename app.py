from flask import Flask, render_template, request, redirect
import sqlite3
import datetime
import os


app = Flask(__name__)

@app.route("/")
def index():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        query1 = """ SELECT building_data_info.BuildingType, buildings.Name, building_data_info.District,
                building_data_info.Price, building_data_info.Sale, building_data_info.Selling FROM building_data_info
                JOIN buildings ON building_data_info.BuildingID = buildings.id
                WHERE buildings.AvailableOnMainPage = '1' AND buildings.BlockedByAdmin = '0'"""
        cursor.execute(query1)
        building_data = cursor.fetchall()
        # print(building_data)
        building_data.reverse()
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        query2 = """ SELECT developer_data.Name FROM developer_data
                JOIN buildings ON developer_data.DeveloperID = buildings.DeveloperID
                WHERE buildings.AvailableOnMainPage = '1' AND buildings.BlockedByAdmin = '0' """
        cursor.execute(query2)
        developer_title = cursor.fetchall()
        developer_title.reverse()
    main_pic = os.listdir(os.path.dirname(__file__) + "/static/developers_database/"
                          + developer_title[0][0] + "/" + building_data[0][1] + "/render/")[0]
    return render_template("index.html", bulding_data=building_data, developer_title=developer_title, main_pic=main_pic)



@app.route("/building/", methods=['GET', 'POST'])
def building():
    if request.method == 'POST':
        return redirect(url_for('index'))


    house = request.args.get("building")
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        query1 = f""" SELECT* FROM building_data_info JOIN buildings ON building_data_info.BuildingID = buildings.id
                WHERE buildings.name = '{house}' """
        cursor.execute(query1)
    house_data = cursor.fetchone()
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        query2 = f""" SELECT developer_data.* FROM developer_data JOIN buildings
        ON developer_data.DeveloperID = buildings.DeveloperID WHERE buildings.name = '{house}' """
        cursor.execute(query2)
    developer = cursor.fetchall()
    # print(developer[0][1], house)

    images = [
        ["/static/developers_database/" + developer[0][1] + "/" + house + "/render/",
         os.listdir(os.path.dirname(__file__) + "/static/developers_database/" + developer[0][1] +
                    "/" + house + "/render/")],
        ["/static/developers_databas/" + developer[0][1] + "/" + house + "/masterplan/",
         os.listdir(os.path.dirname(__file__) + "/static/developers_database/" + developer[0][1] +
                    "/" + house + "/masterplan/")],
        ["/static/developers_database/" + developer[0][1] + "/" + house + "/floor plan/",
         os.listdir(os.path.dirname(__file__) + "/static/developers_database/" + developer[0][1] +
                    "/" + house + "/floor plan/")],
        ["/static/developers_database/" + developer[0][1] + "/" + house + "/apartment plan/",
         os.listdir(os.path.dirname(__file__) + "/static/developers_database/" + developer[0][1] +
                    "/" + house + "/apartment plan/")],
        ["/static/developers_database/" + developer[0][1] + "/" + house + "/progress/",
         os.listdir(os.path.dirname(__file__) + "/static/developers_database/" + developer[0][1] +
                    "/" + house + "/progress/")],]
    # print(images[0][0], images[0][1][0])
    # print(images[0][1])

    return render_template("building.html", name=house, building_data=house_data, developer=developer, images=images )

@app.route("/admin")
def admin():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        query = f""" SELECT Name FROM developer_data """
        cursor.execute(query)
    developers = cursor.fetchall()
    buildings_list = []
    for i in range(len(developers)):
        with sqlite3.connect('database.db') as db:
            cursor = db.cursor()
            query = f""" SELECT buildings.Name, buildings.SubmissionDate FROM buildings
            JOIN developer_data ON buildings.DeveloperID = developer_data.DeveloperID
            WHERE developer_data.Name  = '{developers[i][0]}'"""
            cursor.execute(query)
        houses = cursor.fetchall()
        print(houses)
        buildings_list.append([developers[i][0], houses])
    return render_template("admin.html", data_list=buildings_list)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/developer_exist", methods=["GET", "POST"])
def developer():

    title = request.form.get("title")
    password = request.form.get("pword")
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        query = f""" SELECT * FROM developer_data WHERE Name = '{title}' """
        cursor.execute(query)
    developer = cursor.fetchone()
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        query1 = f""" SELECT buildings.Name FROM buildings JOIN developer_data
        ON buildings.DeveloperID = developer_data.DeveloperID
        WHERE developer_data.Name  = '{title}' """
        cursor.execute(query1)
    houses = cursor.fetchall()

    return render_template("developer.html", developer=developer, houses=houses)

@app.route("/developer_new", methods=["GET", "POST"])
def developer_add():

    title = request.form.get("title")
    phone = request.form.get("phone")
    email = request.form.get("email")
    password = request.form.get("password")

    print(title, phone, email, password)
    developer = ['', title, '', '', '', phone, email,]
    developer_new = ( title, password, phone, email)
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        query = """ INSERT INTO developer_data (Name, Password, PhoneNumber, Email) VALUES(?,?,?,?) """
        cursor.execute(query, developer_new)
        db.commit()
    os.makedirs(os.path.dirname(__file__) + "/static/developers_database/" '/' + title)

    return render_template("developer.html", developer=developer, houses=[])


@app.route("/add_building", methods=["GET", "POST"])
def add_building():
    developer = request.form.get("current_developer")
    print(developer)
    return render_template("add_building.html", developer=developer)


@app.route("/building_added", methods=["GET", "POST"])
def building_added():

    """ Add new building in 'database.db' it table 'buildings'. """
    buildingsName = request.form.get("building_title")
    dev_name = request.form.get("current_developer")
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        query1 = f""" SELECT DeveloperID FROM developer_data WHERE Name = '{dev_name}' """
        cursor.execute(query1)
        buildingsDeveloperID = cursor.fetchone()
    buildings_data = (buildingsName, buildingsDeveloperID[0], datetime.datetime.now(), 1, 0)
    # print(buildings_data)
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        query2 = """ INSERT INTO buildings (
                Name, DeveloperID, SubmissionDate, AvailableOnMainPage, BlockedByAdmin)
                VALUES(?,?,?,?,?) """
        cursor.execute(query2, buildings_data)
        db.commit()

    """ Add building's data in 'database.db' it table 'building_data_info'. """
    bdiBuildingType = request.form.get("building_type")
    bdiDistrict = request.form.get("district")
    bdiStreet = request.form.get("street")
    bdiStreetNumber = request.form.get("street_number")
    bdiStatus = request.form.get("status")
    bdiPrice = request.form.get("price")
    bdiSelling = int(request.form.get("selling"))
    bdiRoom1 = 1 if request.form.get("room1") == '1' else 0
    bdiRooms2 = 1 if request.form.get("room2") == '1' else 0
    bdiRooms3 = 1 if request.form.get("room3") == '1' else 0
    bdiRooms4 = 1 if request.form.get("room4") == '1' else 0
    bdiParking = 1 if request.form.get("parking") == '1' else 0
    bdiCommercial = 1 if request.form.get("commercial") == '1' else 0
    bdiNumberOfFloors = int(request.form.get("floor_qty"))
    bdiTechnology = request.form.get("technology")
    bdiWalls = request.form.get("walls")
    bdiInsulation = request.form.get("insulation")
    bdiHeating = request.form.get("heating")
    bdiRoomHeight = float(request.form.get("room_height"))
    bdiDescription = request.form.get("description")
    bdiSale = 1 if request.form.get("sale_description") != '' else 0
    bdiSaleDescription = request.form.get("sale_description")

    buildings_info = (bdiBuildingType, bdiDistrict, bdiStreet, bdiStreetNumber, bdiStatus, bdiPrice, bdiSelling,
                      bdiRoom1, bdiRooms2, bdiRooms3, bdiRooms4, bdiParking, bdiCommercial, bdiNumberOfFloors,
                      bdiTechnology, bdiWalls, bdiInsulation, bdiHeating, bdiRoomHeight, bdiDescription, bdiSale,
                      bdiSaleDescription)
    # print(buildings_info)
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        query3 = """ INSERT INTO building_data_info (
                BuildingType, District, Street, StreetNumber, Status, Price, Selling,
                Room1, Rooms2, Rooms3, Rooms4, Parking, Commercial, NumberOfFloors,
                Technology, Walls, Insulation, Heating, RoomHeight, Description, Sale, SaleDescription)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """
        cursor.execute(query3, buildings_info)
        db.commit()

    """ Create folders for images. """
    for i in ('render', 'floor plan', 'apartment plan', 'masterplan', 'progress'):
        os.makedirs(os.path.dirname(__file__) + "/static/developers_database/" + dev_name +
                    '/' + buildingsName + '/' + i)

    """ Add images to folders."""
    if request.files:
        for image in request.files.getlist("renders"):
            image.save(os.path.join(os.path.dirname(__file__) + "/static/developers_database/" + dev_name + '/'
                                    + buildingsName + '/render', image.filename))
        for image in request.files.getlist("floor_plans"):
            image.save(os.path.join(os.path.dirname(__file__) + "/static/developers_database/" + dev_name + '/'
                                    + buildingsName + '/floor plan', image.filename))
        for image in request.files.getlist("apartment_plans"):
            image.save(os.path.join(os.path.dirname(__file__) + "/static/developers_database/" + dev_name + '/'
                                    + buildingsName + '/apartment plan', image.filename))
        for image in request.files.getlist("masterplans"):
            image.save(os.path.join(os.path.dirname(__file__) + "/static/developers_database/" + dev_name + '/'
                                    + buildingsName + '/masterplan', image.filename))
        for image in request.files.getlist("progres"):
            image.save(os.path.join(os.path.dirname(__file__) + "/static/developers_database/" + dev_name + '/'
                                    + buildingsName + '/progress', image.filename))

    return render_template("building_added.html")

@app.route("/search_results", methods=["GET", "POST"])
def search():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        query = """ SELECT buildings.Name, building_data_info.District, building_data_info.Room1,
        building_data_info.Rooms2, building_data_info.Rooms3, building_data_info.Rooms4,
        building_data_info.Parking, building_data_info.Commercial, building_data_info.NumberOfFloors
        FROM building_data_info JOIN buildings ON building_data_info.BuildingID = buildings.id
        WHERE buildings.AvailableOnMainPage = '1' AND buildings.BlockedByAdmin = '0'"""
        cursor.execute(query)
    all_buildings = cursor.fetchall()

    """ Step 1 - search by district. """
    buildings_by_district = []
    if request.form.get("district1") == '1' or request.form.get("district2") == '1' \
            or request.form.get("district3") == '1' or request.form.get("district4") == '1' \
            or request.form.get("district5") == '1' or request.form.get("district6") == '1':
        if request.form.get("district1") == '1':
            for i in all_buildings:
                if i[1] == 'Галицький': buildings_by_district.append(i)
        if request.form.get("district2") == '1':
            for i in all_buildings:
                if i[1] == 'Залізничний': buildings_by_district.append(i)
        if request.form.get("district3") == '1':
            for i in all_buildings:
                if i[1] == 'Личаківський': buildings_by_district.append(i)
        if request.form.get("district4") == '1':
            for i in all_buildings:
                if i[1] == 'Сихівський': buildings_by_district.append(i)
        if request.form.get("district5") == '1':
            for i in all_buildings:
                if i[1] == 'Франківський': buildings_by_district.append(i)
        if request.form.get("district6") == '1':
            for i in all_buildings:
                if i[1] == 'Шевченківський': buildings_by_district.append(i)
    # print(buildings_by_district)

    """ Step 2 - search by flat. """
    buildings_by_rooms = []
    if request.form.get("rooms1") == '1' or request.form.get("rooms2") == '1' \
            or request.form.get("rooms3") == '1' or request.form.get("rooms4") == '1' \
            or request.form.get("rooms5") == '1' or request.form.get("rooms6") == '1':
        if request.form.get("rooms1") == '1':
            for i in all_buildings:
                if i[2] == 1: buildings_by_rooms.append(i)
        if request.form.get("rooms2") == '1':
            for i in all_buildings:
                if i[3] == 1: buildings_by_rooms.append(i)
        if request.form.get("rooms3") == '1':
            for i in all_buildings:
                if i[4] == 1: buildings_by_rooms.append(i)
        if request.form.get("rooms4") == '1':
            for i in all_buildings:
                if i[5] == 1: buildings_by_rooms.append(i)
        if request.form.get("rooms5") == '1':
            for i in all_buildings:
                if i[6] == 1: buildings_by_rooms.append(i)
        if request.form.get("rooms6") == '1':
            for i in all_buildings:
                if i[7] == 1: buildings_by_rooms.append(i)
    # print(buildings_by_rooms)

    """ Step 3 - search by floors. """
    buildings_by_floors = []
    if request.form.get("floors1") == '1' or request.form.get("floors2") == '1' \
            or request.form.get("floors3") == '1' or request.form.get("floors4") == '1':
        if request.form.get("floors1") == '1':
            for i in all_buildings:
                if i[8] < 6: buildings_by_floors.append(i)
        if request.form.get("floors2") == '1':
            for i in all_buildings:
                if i[8] > 5 and i[8] < 10: buildings_by_floors.append(i)
        if request.form.get("floors3") == '1':
            for i in all_buildings:
                if i[8] > 9 and i[8] < 17: buildings_by_floors.append(i)
        if request.form.get("floors4") == '1':
            for i in all_buildings:
                if i[8] > 16: buildings_by_floors.append(i)
    # print(buildings_by_floors)

    if len(buildings_by_district) == 0:
        if request.form.get("district1") == '1' or request.form.get("district2") == '1' \
                or request.form.get("district3") == '1' or request.form.get("district4") == '1' \
                or request.form.get("district5") == '1' or request.form.get("district6") == '1':
            return render_template("no_results.html")
        else:
            if len(buildings_by_rooms) == 0:
                if request.form.get("rooms1") == '1' or request.form.get("rooms2") == '1' \
                        or request.form.get("rooms3") == '1' or request.form.get("rooms4") == '1' \
                        or request.form.get("rooms5") == '1' or request.form.get("rooms6") == '1':
                    return render_template("no_results.html")
                else:
                    if len(buildings_by_floors) == 0:
                        if request.form.get("floors1") == '1' or request.form.get("floors2") == '1' \
                                or request.form.get("floors3") == '1' or request.form.get("floors4") == '1':
                            return render_template("no_results.html")
                        else:
                            return redirect("/")
                    else:
                        buildings_by_district = all_buildings
                        buildings_by_rooms = all_buildings
            else:
                buildings_by_district = all_buildings
                if len(buildings_by_floors) == 0:
                    if request.form.get("floors1") == '1' or request.form.get("floors2") == '1' \
                            or request.form.get("floors3") == '1' or request.form.get("floors4") == '1':
                        return render_template("no_results.html")
                    else:
                        buildings_by_floors = all_buildings
    else:
        if len(buildings_by_rooms) == 0:
            if request.form.get("rooms1") == '1' or request.form.get("rooms2") == '1' \
                    or request.form.get("rooms3") == '1' or request.form.get("rooms4") == '1' \
                    or request.form.get("rooms5") == '1' or request.form.get("rooms6") == '1':
                return render_template("no_results.html")
            else:
                buildings_by_rooms = all_buildings
        if len(buildings_by_floors) == 0:
            if request.form.get("floors1") == '1' or request.form.get("floors2") == '1' \
                    or request.form.get("floors3") == '1' or request.form.get("floors4") == '1':
                return render_template("no_results.html")
            else:
                buildings_by_floors = all_buildings
    # print(buildings_by_district)
    # print(buildings_by_rooms)
    # print(buildings_by_floors)

    buildings_for_search = []
    for i in all_buildings:
        if i in buildings_by_district and i in buildings_by_rooms and i in buildings_by_floors:
            buildings_for_search.append(i[0])

    if len(buildings_for_search) > 0:
        with sqlite3.connect('database.db') as db:
            cursor = db.cursor()
            query = """ SELECT building_data_info.BuildingType, buildings.Name, building_data_info.District,
                    building_data_info.Price, building_data_info.Sale, building_data_info.Selling, developer_data.Name
                    FROM building_data_info
                    JOIN buildings ON building_data_info.BuildingID = buildings.id
                    JOIN developer_data ON developer_data.DeveloperID = buildings.DeveloperID
                    WHERE buildings.AvailableOnMainPage = '1' AND buildings.BlockedByAdmin = '0'"""
            cursor.execute(query)
            buildings_data = cursor.fetchall()
        # print(buildings_data)
        buildings_list = []
        for j in buildings_data:
            if j[1] in buildings_for_search: buildings_list.append(j)
        # print(buildings_list)
        buildings_list.reverse()
        main_pic = os.listdir(os.path.dirname(__file__) + "/static/developers_database/"
                              + buildings_list[0][6] + "/" + buildings_list[0][1] + "/render/")[0]
        return render_template("search_results.html", bulding_data=buildings_list, main_pic=main_pic)
    else:
        return render_template("no_results.html")

@app.route("/my_buildings", methods=["GET", "POST"])
def my_buildings():
    buildings_mine = ['Пасічна 25А', 'Скрипника-Освицька', 'Наукова 2Д', 'Личаківська перлина', 'Дж. Вашингтона',
                      'Манастирського', 'Софіївка', 'Globus Elite 2', 'Софіївка 2']
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        query = """ SELECT building_data_info.BuildingType, buildings.Name, building_data_info.District,
                building_data_info.Price, building_data_info.Sale, building_data_info.Selling, developer_data.Name
                FROM building_data_info
                JOIN buildings ON building_data_info.BuildingID = buildings.id
                JOIN developer_data ON developer_data.DeveloperID = buildings.DeveloperID
                WHERE buildings.AvailableOnMainPage = '1' AND buildings.BlockedByAdmin = '0'"""
        cursor.execute(query)
        buildings_data = cursor.fetchall()
    buildings_list = []
    for i in buildings_data:
        if i[1] in buildings_mine: buildings_list.append(i)
    buildings_list.reverse()
    main_pic = os.listdir(os.path.dirname(__file__) + "/static/developers_database/"
                          + buildings_list[0][6] + "/" + buildings_list[0][1] + "/render/")[0]
    return render_template("search_results.html", bulding_data=buildings_list, main_pic=main_pic)


if __name__ == "__main__":
    app.run(debug=True)
