tables = {
    'create_query':  {
        'google':"""
            CREATE TABLE google (
                location VARCHAR(30),
                name VARCHAR(150),
                reviewId VARCHAR(80) PRIMARY KEY,
                reviewer VARCHAR(300),
                starRating VARCHAR(5),
                comment VARCHAR(4000),
                createTime VARCHAR(25),
                updateTime VARCHAR(25)
            );
        """,
        'tripadvisor':"""
            CREATE TABLE tripadvisor (
                id INTEGER PRIMARY KEY,
                link VARCHAR(139),
                restaurant VARCHAR(23),
                title VARCHAR(150),
                date VARCHAR(17),
                visit_date VARCHAR(14),
                review VARCHAR(11336),
                score INTEGER,
                value INTEGER,
                service INTEGER,
                food INTEGER,
                response VARCHAR(3401)
            );
        """,
        'opentable':"""
            CREATE TABLE opentable (
                restaurant VARCHAR(27),
                name VARHCAR(25),
                dined_date VARCHAR(17),
                overall_score INTEGER,
                food_score INTEGER,
                service_score INTEGER,
                ambience_score INTEGER,
                review_text VARCHAR(2000),
                id VARCHAR(65) PRIMARY KEY
            );
        """,
        'sevenrooms':"""
            CREATE TABLE sevenrooms (
                reservation_id VARHCAR(84) PRIMARY KEY,
                restaurant VARHCAR(34),
                received_date VARCHAR(10),
                reservation_date VARCHAR(10),
                overall INTEGER,
                food INTEGER,
                service INTEGER,
                ambience INTEGER,
                recommend_to_friend VARCHAR(15)
            );
        """,
        'reviews':"""
            CREATE TABLE reviews (
                source VARCHAR(11),
                restaurant VARCHAR(25),
                title VARCHAR(150),
                date VARCHAR(10),
                score INTEGER,
                food INTEGER,
                service INTEGER,
                value INTEGER,
                ambience INTEGER,
                review TEXT,
                link TEXT
            );
        """,
        'scores':"""
            CREATE TABLE scores (
                restaurant VARCHAR(25),
                date VARCHAR(10),
                score INTEGER,
                food INTEGER,
                service INTEGER,
                value INTEGER,
                ambience INTEGER,
            );
        """
    },
    'columns': {
        'google':[
            'location',
            'name',
            'review_id',
            'reviewer_display_name',
            'star_rating',
            'comment',
            'create_time',
            'update_time',
            'link',
        ],
        'tripadvisor':[
            'id',
            'link',
            'restaurant',
            'title',
            'date',
            'visit_date',
            'review',
            'score',
            'value',
            'service',
            'food',
            'response',
        ],
        'opentable':[
            'restaurant',
            'name',
            'date',
            'dined_date',
            'overall_score',
            'food_score',
            'service_score',
            'ambience_score',
            'review_text',
            'id',
            'link',
        ],
        'sevenrooms': [
            'reservation_id',
            'restaurant',
            'received_date',
            'reservation_date',
            'overall',
            'food',
            'service',
            'ambience',
            'recommend_to_friend',
            'notes',
            'link',
        ],
        'reviews': [
            'source',
            'restaurant',
            'title',
            'date',
            'visit_date',
            'score',
            'food',
            'service',
            'value',
            'ambience',
            'review',
            'link',
        ],
        'scores': [
            'restaurant',
            'date',
            'score',
            'food',
            'service',
            'value',
            'ambience',
        ],
    },
    'null_columns': {
        'google': 'comment',
        'tripadvisor':'response',
        'opentable':'',
        'sevenrooms':'notes',
    },
    'rename_columns': {
        'google':{
            'reviewId':'review_id',
            'starRating':'star_rating',
            'createTime':'create_time',
            'updateTime':'update_time'
        }
    },
    'to_master_database_maps':{
        'restaurant':{
            'opentable':{
                '100 Wardour Street Club': '100 Wardour Street',
                '100 Wardour Street Lounge': '100 Wardour Street',
                '14 Hills': '14 Hills',
                '20 Stories': '20 Stories',
                'Angelica': 'Angelica',
                'Angler': 'Angler',
                'Aster Cafe': 'Aster',
                'Aster Restaurant': 'Aster',
                'Avenue': 'Avenue',
                'Bluebird Chelsea': 'Bluebird Chelsea',
                'Bluebird White City': 'Bluebird White City',
                'Butlers Wharf Chophouse': 'Butlers Wharf Chophouse',
                'Cantina': 'Cantina',
                'Crafthouse':'Crafthouse',
                "Coq d'Argent Grill": "Coq d'Argent",
                "Coq d'Argent Restaurant": "Coq d'Argent",
                'East 59th': 'East 59th',
                'Fish Market': 'Fish Market',
                'Fiume': 'Fiume',
                'German Gymnasium Cafe': 'German Gymnasium',
                'German Gymnasium Restaurant': 'German Gymnasium',
                'Issho': 'Issho',
                'Klosterhaus': 'Klosterhaus',
                'Launceston Place': 'Launceston Place',
                'Le Pont de la Tour': 'Le Pont de la Tour',
                'Madison': 'Madison',
                'New Street Grill': 'New Street Grill',
                'Orrery': 'Orrery',
                'Paternoster Chophouse': 'Paternoster Chophouse',
                'Plateau': 'Plateau',
                "Quaglino's": "Quaglino's",
                'Radici': 'Radici',
                'Sartoria': 'Sartoria',
                'Skylon': 'Skylon',
                'South Place Chop House': 'South Place Chop House',
                'The Modern Pantry': 'The Modern Pantry',
            },
            'google':{
                '100 Wardour Street': '100 Wardour Street',
                '14 Hills': '14 Hills',
                '20 Stories': '20 Stories',
                'Angelica': 'Angelica',
                'Angler': 'Angler',
                'Aster': 'Aster',
                'Avenue': 'Avenue',
                'Bluebird Café White City': 'Bluebird White City',
                'Bluebird Chelsea': 'Bluebird Chelsea',
                'Bluebird London NYC': 'Bluebird London NYC',
                'Blueprint Café': 'Blueprint Café',
                'Butlers Wharf Chop House': 'Butlers Wharf Chophouse',
                'Cantina Del Ponte': 'Cantina',
                "Coq d'Argent": "Coq d'Argent",
                'Crafthouse': 'Crafthouse',
                'D & D London Ltd': 'D & D London Ltd',
                'East 59th': 'East 59th',
                'Fish Market': 'Fish Market',
                'Fiume': 'Fiume',
                'German Gymnasium Grand Café': 'German Gymnasium',
                'Issho Rooftop Restaurant & Bar': 'Issho',
                'Klosterhaus': 'Klosterhaus',
                'Launceston Place': 'Launceston Place',
                'Le Pont de la Tour': 'Le Pont de la Tour',
                'Madison': 'Madison',
                'New Street Grill': 'New Street Grill',
                'New Street Wine': 'New Street Wine',
                'Old Bengal Bar': 'Old Bengal Bar',
                'Orrery': 'Orrery',
                'Orrery Epicerie': 'Orrery',
                'Paternoster Chop House': 'Paternoster Chophouse',
                'Plateau': 'Plateau',
                "Quaglino's": "Quaglino's",
                'Radici': 'Radici',
                'Royal Exchange Grand Café': 'Royal Exchange Grand Café',
                'Sartoria': 'Sartoria',
                'Skylon': 'Skylon',
                'The Den': 'The Den',
                'The Modern Pantry': 'The Modern Pantry',
                'queensyard': 'queensyard'
            },
            'sevenrooms':{
                '100 Wardour St. Restaurant & Club': '100 Wardour Street',
                '100 Wardour Street Bar & Lounge': '100 Wardour Street',
                '14 Hills': '14 Hills',
                '20 Stories': '20 Stories',
                'Angelica': 'Angelica',
                'Angler Restaurant': 'Angler',
                'Aster Cafe': 'Aster',
                'Aster Restaurant': 'Aster',
                'Avenue': 'Avenue',
                'Bluebird Chelsea Café': 'Bluebird Chelsea',
                'Bluebird Chelsea Restaurant': 'Bluebird Chelsea',
                'Bluebird White City': 'Bluebird White City',
                'Blueprint Café': 'Blueprint Café',
                'Butlers Wharf Chophouse Restaurant': 'Butlers Wharf Chophouse',
                'Cantina del Ponte': 'Cantina',
                "Coq d'Argent Grill": "Coq d'Argent",
                "Coq d'Argent Restaurant": "Coq d'Argent",
                'Crafthouse': 'Crafthouse',
                'East 59th': 'East 59th',
                'Fish Market': 'Fish Market',
                'Fiume': 'Fiume',
                'German Gymnasium Restaurant': 'German Gymnasium',
                'Grand Café & Restaurant': 'German Gymnasium',
                'Issho Bar': 'Issho',
                'Issho Restaurant': 'Issho',
                'Klosterhaus': 'Klosterhaus',
                'Launceston Place': 'Launceston Place',
                'Madison Restaurant': 'Madison',
                'Madison Restaurant and Bar': 'Madison',
                'New Street Grill': 'New Street Grill',
                'Orrery': 'Orrery',
                'Paternoster Chophouse': 'Paternoster Chophouse',
                'Plateau Restaurant': 'Plateau',
                'Plateau Terrace': 'Plateau',
                'Pont de la Tour Bar & Grill': 'Le Pont de la Tour',
                'Pont de la Tour Restaurant': 'Le Pont de la Tour',
                'Quaglino’s Restaurant': "Quaglino's",
                'Radici': 'Radici',
                'Sartoria': 'Sartoria',
                'Skylon Restaurant': 'Skylon',
                'South Place Chop House': 'South Place Chop House',
                'The Modern Pantry': 'The Modern Pantry',
                'The Secret Garden': 'The Secret Garden'
            },
        },
        'rename_columns': {
            'opentable': {
                'dined_date':'visit_date',
                'name':'title',
                'overall_score':'score',
                'food_score':'food',
                'service_score':'service',
                'ambience_score':'ambience',
                'review_text':'review'
            },
            'google': {
                'location':'restaurant',
                'review_id':'id',
                'reviewer_display_name':'title',
                'star_rating':'score',
                'comment':'review',
                'review_reply':'response',
                'create_time':'date'
            },
            'sevenrooms': {
                'received_date':'date',
                'reservation_id':'title',
                'reservation_date':'visit_date',
                'overall':'score',
                'notes':'review'
            }            
        }
    }
}