restaurant_list = {
    '100 Wardour Street': 1,
    '14 Hills': 2,
    '20 Stories': 3,
    'Angelica': 4,
    'Angler': 5,
    'Aster': 6,
    'Avenue': 7,
    'Bluebird Chelsea': 8,
    'Bluebird White City': 9,
    'Blueprint Café': 10,
    'Butlers Wharf Chophouse': 11,
    'Cantina': 12,
    "Coq d'Argent": 13,
    'Crafthouse': 14,
    'East 59th': 15,
    'Fish Market': 16,
    'Fiume': 17,
    'German Gymnasium': 18,
    'Issho': 19,
    'Klosterhaus': 20,
    'Launceston Place': 21,
    'Le Pont de la Tour': 22,
    'Madison': 23,
    'New Street Grill': 24,
    'New Street Wine': 25,
    'Old Bengal Bar': 26,
    'Orrery': 27,
    'Paternoster Chophouse': 28,
    'Plateau': 29,
    "Quaglino's": 30,
    'Radici': 31,
    'Sartoria': 32,
    'Skylon': 33,
    'South Place Chophouse': 34,
    'The Modern Pantry': 35
}

managers = [
    'Dainius Kazlauska',
    'Massimiliano Deiana',
    'Kim Sin Tae',
    'Med Rogers',
    'Vidmantas Gricius',
    'Carlo Scalzotto',
    'Ismael Nuha',
    'Enrico Bucci',
    'Vito Centrone',
    'Michar Buzzola',
    'Anna Popiel',
    'Ornets Freimanis',
    'Imants Zusmanis',
    'Olga Gay',
    'Sam Bernard',
    'Rad Kapinos',
    'Tiago Pinto',
    'Alfonso Cadena',
    'Philip Urasala',
    'Eddy Ferrouillat',
    'Sean Gavin',
    'Guillaume Sanzey',
    'William Gomis',
    'Jonathan Payan',
    'Susanne Traudt',
    'Susanne Traudt'
]

ops_director_strins = [
    'Michael Farquhar',
    'JB Requien',
    'Sharon Whiston'
]

users = [
    {
        'email':manager.split(' ')[0].lower() + manager.split(' ')[1][0].lower() + '@danddlondon.com',
        'first_name':manager.split(' ')[0],
        'last_name':manager.split(' ')[1]
    } for manager in managers
]

restaurant_dict = {'100 Wardour Street': {'id': 1,
  'manager': {'email': 'kims@danddlondon.com', 'name': 'Kim Sin Tae'},
  'director': 'michaelf@danddlondon.com'},
 '14 Hills': {'id': 2,
  'manager': {'email': 'massimilianod@danddlondon.com',
   'name': 'Massimiliano Deiana'},
  'director': 'michaelf@danddlondon.com'},
 '20 Stories': {'id': 3,
  'manager': {'email': 'philipu@danddlondon.com', 'name': 'Philip Urasala'},
  'director': 'jb@danddlondon.com'},
 'Angelica': {'id': 4,
  'manager': {'email': 'guillaumes@danddlondon.com',
   'name': 'Guillaume Sanzey'},
  'director': 'jb@danddlondon.com'},
 'Angler': {'id': 5,
  'manager': {'email': 'susannet@danddlondon.com', 'name': 'Susanne Traudt'},
  'director': 'jb@danddlondon.com'},
 'Aster': {'id': 6,
  'manager': {'email': 'radk@danddlondon.com', 'name': 'Rad Kapinos'},
  'director': 'jb@danddlondon.com'},
 'Avenue': {'id': 7,
  'manager': {'email': 'joseu@danddlondon.com', 'name': 'Jose Ubero'},
  'director': 'michaelf@danddlondon.com'},
 'Bluebird Chelsea': {'id': 8,
  'manager': {'email': 'mattm@danddlondon.com', 'name': 'Matthew Maynard'},
  'director': 'michaelf@danddlondon.com'},
 'Bluebird White City': {'id': 9,
  'manager': {'email': 'matteol@danddlondon.com', 'name': 'Matteo Lazarian'},
  'director': 'michaelf@danddlondon.com'},
 'Blueprint Café': {'id': 10,
  'manager': {'email': 'carlaa@danddlondon.com', 'name': 'Carla Amaro'},
  'director': 'sharonw@danddlondon.com'},
 'Butlers Wharf Chophouse': {'id': 11,
  'manager': {'email': 'imantsz@danddlondon.com', 'name': 'Imants Zusmanis'},
  'director': 'sharonw@danddlondon.com'},
 'Cantina': {'id': 12,
  'manager': {'email': 'ornetsf@danddlondon.com', 'name': 'Ornets Freimanis'},
  'director': 'sharonw@danddlondon.com'},
 "Coq d'Argent": {'id': 13,
  'manager': {'email': 'seang@danddlondon.com', 'name': 'Sean Gavin'},
  'director': 'jb@danddlondon.com'},
 'Crafthouse': {'id': 14,
  'manager': {'email': 'crafthouse@danddlondon.com',
   'name': 'Crafthouse Manager'},
  'director': 'jb@danddlondon.com'},
 'East 59th': {'id': 15,
  'manager': {'email': 'jonathanp@danddlondon.com', 'name': 'Jonathan Payan'},
  'director': 'jb@danddlondon.com'},
 'Fish Market': {'id': 16,
  'manager': {'email': 'eddyf@danddlondon.com', 'name': 'Eddy Ferrouillat'},
  'director': 'jb@danddlondon.com'},
 'Fiume': {'id': 17,
  'manager': {'email': 'micharb@danddlondon.com', 'name': 'Michar Buzzola'},
  'director': 'sharonw@danddlondon.com'},
 'German Gymnasium': {'id': 18,
  'manager': {'email': 'samb@danddlondon.com', 'name': 'Sam Bernard'},
  'director': 'jb@danddlondon.com'},
 'Issho': {'id': 19,
  'manager': {'email': 'williamg@danddlondon.com', 'name': 'William Gomis'},
  'director': 'jb@danddlondon.com'},
 'Klosterhaus': {'id': 20,
  'manager': {'email': 'tiago@danddlondon.com', 'name': 'Tiago Pinto'},
  'director': 'jb@danddlondon.com'},
 'Launceston Place': {'id': 21,
  'manager': {'email': 'carlos@danddlondon.com', 'name': 'Carlo Scalzotto'},
  'director': 'sharonw@danddlondon.com'},
 'Le Pont de la Tour': {'id': 22,
  'manager': {'email': 'olgag@danddlondon.com', 'name': 'Olga Gay'},
  'director': 'sharonw@danddlondon.com'},
 'Madison': {'id': 23,
  'manager': {'email': 'medr@danddlondon.com', 'name': 'Med Rogers'},
  'director': 'michaelf@danddlondon.com'},
 'New Street Grill': {'id': 24,
  'manager': {'email': 'someguy@danddlondon.com', 'name': 'NSG Manager'},
  'director': 'jb@danddlondon.com'},
 'New Street Wine': {'id': 25,
  'manager': {'email': 'nsw@danddlondon.com', 'name': 'NSW Manager'},
  'director': 'jb@danddlondon.com'},
 'Old Bengal Bar': {'id': 26,
  'manager': {'email': 'obbf@danddlondon.com', 'name': 'OBB Manager'},
  'director': 'jb@danddlondon.com'},
 'Orrery': {'id': 27,
  'manager': {'email': 'ismaeln@danddlondon.com', 'name': 'Fadil Nuha'},
  'director': 'sharonw@danddlondon.com'},
 'Paternoster Chophouse': {'id': 28,
  'manager': {'email': 'emilie@danddlondon.com',
   'name': 'Emilie Parker Smith'},
  'director': 'jb@danddlondon.com'},
 'Plateau': {'id': 29,
  'manager': {'email': 'alfonsoc@danddlondon.com', 'name': 'Alfonso Cadena'},
  'director': 'jb@danddlondon.com'},
 "Quaglino's": {'id': 30,
  'manager': {'email': 'vidmantasg@danddlondon.com',
   'name': 'Vidmantas Gricius'},
  'director': 'michaelf@danddlondon.com'},
 'Radici': {'id': 31,
  'manager': {'email': 'vitoc@danddlondon.com', 'name': 'Vito Centrone'},
  'director': 'sharonw@danddlondon.com'},
 'Sartoria': {'id': 32,
  'manager': {'email': 'enricob@danddlondon.com', 'name': 'Enrico Bucci'},
  'director': 'sharonw@danddlondon.com'},
 'Skylon': {'id': 33,
  'manager': {'email': 'dainiusk@danddlondon.com',
   'name': 'Dainius Kazlauska'},
  'director': 'michaelf@danddlondon.com'},
 'South Place Chophouse': {'id': 34,
  'manager': {'email': 'thomass@danddlondon.com', 'name': 'Thomas Scheurch'},
  'director': 'jb@danddlondon.com'},
 'The Modern Pantry': {'id': 35,
  'manager': {'email': 'annap@danddlondon.com', 'name': 'Anna Popiel'},
  'director': 'sharonw@danddlondon.com'}}    