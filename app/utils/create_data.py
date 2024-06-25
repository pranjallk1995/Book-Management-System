""" module to create tables and its entries for first run """

import logging as lg
import config as cfg
import asyncpg as apg
class CreateData():
    """ create the bookstore database schema and book data """

    def __init__(self) -> None:
        self.user = cfg.DATABASE_USER
        self.password = cfg.DATABASE_USER_PASSWORD
        self.database = cfg.DATABASE_NAME
        self.host = cfg.DATABASE_SERVICE
        self.connection = None

    def check_status(self, status: str, table: cfg.DatabaseTables) -> None:
        """ check if creating table was successful """
        if "NOTICE" not in status:
            lg.info(" Table: %s has been created", table.value)
        elif "NOTICE" in status:
            lg.info(" Table: %s already exists", table.value)
        elif "INSERT" in status:
            lg.info(" Default data added to Table: %s", table.value)
        else:
            lg.error(" Failed to create Table: %s", table.value)

    async def create_tables(self) -> None:
        """ function to create tables if they do not exist """

        genres = ", ".join(["'"+genre.value+"'" for genre in cfg.Genres])
        ratings = ", ".join([str(rating.value) for rating in cfg.Ratings])

        create_book_table = f"""
            CREATE TABLE IF NOT EXISTS {cfg.DatabaseTables.BOOKS.value}(
                id serial PRIMARY KEY,
                title varchar(255) NOT NULL,
                author varchar(255) NOT NULL,
                genre varchar(20),
                year_published DATE,
                summary varchar(8000),
                CONSTRAINT check_genre CHECK (genre IN ({genres}))
            );
        """

        create_reviews_table = f"""
            CREATE TABLE IF NOT EXISTS {cfg.DatabaseTables.REVIEWS.value}(
                id serial PRIMARY KEY,
                book_id int,
                user_id int NOT NULL,
                review_text varchar(8000),
                rating int,
                FOREIGN KEY (book_id) REFERENCES books(id),
                CONSTRAINT check_rating CHECK (rating IN ({ratings}))
            );
        """

        create_status = await self.connection.execute(create_book_table)
        self.check_status(create_status, cfg.DatabaseTables.BOOKS)

        create_status = await self.connection.execute(create_reviews_table)
        self.check_status(create_status, cfg.DatabaseTables.REVIEWS)

    async def create_data(self) -> None:
        """ function to add default data into database """

        add_book_data = f"""
            INSERT INTO {cfg.DatabaseTables.BOOKS.value}(title, author, genre, year_published, summary) VALUES (
                'The Story of You - Bio Computer', 'Kura Venkateswara Reddy', 'Science',
                '2021-03-08', 'Our intent is to bring a quest in knowing “YOU”, by yourself in the form of the book
                The Story of You - Bio Computer. It is the first step in putting tiny wisdom through a lens of
                Spirituality, Science, History and Digital technologies. This book is for everyone, transcending
                geographies, organizations, governments, religions, languages, caste, countries, rich, poor, and so on.
                If you are not spending enough time to understand scientifically Who “YOU” are then you are wasting your
                life, irrespective of whatever the position, power, role, status and wealth etc. you hold in the external
                world. You are an individual Bio Computer in a complex web -controlled by Artificial Intelligence and
                10 programs through seven bodies of YOU. It is possible to change some of these programs, and other global
                programs that need to be de-clutched and configured to the right IP address. One of the purposes of this
                book is to make you realize intellectually that, as an individual edge device or Bio Computer YOU are
                helpless, and YOU must realize that there is “NO YOU “. That is when you surrender with true wisdom.
                This is a magnificent creation and evolved over billions of years. If you are not experiencing this
                creation and higher levels of Consciousness, you are just dying like a worm.  Make use of the remaining
                few years of your life.  Firstly, try to become awakened and live the life of an enlightened being while
                you are on this planet. Human beings are designed to be enlightened. Secondly this could be the last life
                on this planet for you.'
            ), (
                'The Power of Your Subconscious Mind', 'Joseph Murphy', 'Science',
                '2015-02-01', 'This remarkable book by Dr. Joseph Murphy, one of the pioneering voices of affirmative thinking,
                will unlock for you the truly staggering powers of your subconscious mind. Combining time-honored spiritual
                wisdom with cutting edge scientific research, Dr. Murphy explains how the subconscious mind influences every
                single thing that you do and how, by understanding it and learning to control its incredible force, you can
                improve the quality of your daily life.Everything, from the promotion that you wanted and the raise you think you
                deserve, to overcoming phobias and bad habits and strengthening interpersonal relationships, the Power of Your
                Subconscious Mind will open a world of happiness, success, prosperity and peace for you. It will change your life
                and your world by changing your beliefs.'
            ), (
                'Stop Overthinking', 'Nick Trenton', 'Science',
                '2021-01-01', 'Break free of your self-imposed mental prison. Stop agonizing over the past and trying to predict
                the future. Overthinking is the biggest cause of unhappiness and staying in a never-ending thought loop is the biggest
                cause of unhappiness. Stop Overthinking is a book that understands the exhausting situation you have put yourself in,
                and how you lose your mind with anxiety and stress. It will walk you through detailed and proven techniques to help
                rewire your brain, control your thoughts, and change your mental habits.'
            );
        """

        add_review_data = f"""
            INSERT INTO {cfg.DatabaseTables.REVIEWS.value}(book_id, user_id, review_text, rating) VALUES (
                '1', '1', 'Author has put in integrated wisdom across many subjects and we realize Oneness in all these fields. I had
                lot of confusion about enlightenment and after death what next etc. After going through one Chapter in this book
                Consciousness – now I could understand intellectually, scientifically what this all about Awakening, Enlightenment, Oneness
                and Light being and what should we purse as objective after our death – attaining Moksha. Thank You. I want enlarge
                these color diagrams and laminate them. Beautifully explained through color pictures, worth gifting. I wish this book
                should be ETERNAL for humanity.', '5'
            ), (
                '1', '2', 'Excellent book in connecting quantum mechanics, vibrations,fractals, epigenetics, Digital technologies
                like Cloud, AI, VR, and Spirituality . Spirituality is the Science, this should have been a compulsory subject that
                every student on this Planet to go through in High School studies . It is a greatest gift for the present and future
                generations. Please give this book as gift to children , even before you read.', '5'
            ), (
                '1', '3', 'Namasteji, This BOOK is unexplainable, it should be experienced each and every sentence, Spiritually,
                Physically in the life. THE GRACE & THE PRESENCE of SRI SRI AMMABHAGAVAN are flowing through YOU & YOUR BOOK.
                Many,many thanks to you & your family members, your ancestors & your team. AMMABHAGAVAN BLESS YOU & YOUR FAMILY.', '5'
            ), (
                '2', '3', 'Loved it :)', '4'
            ), (
                '2', '4', 'I didnt like the read to be honest, the author has no concrete points to make or teach through his book
                rather he has taken a lot of biblical verses and kept on praising it for some weird reasons With very minimal content
                to learn from, he tried his best to link it with conscious and subconscious thoughts and concepts which I found was
                absurd coz he didnt do it well and science could explain it well. As an Indian I feel reading our own philosophical
                books would make much sense and would be relatable than reading this. It was my worst read till tills day, never
                buying a book from these western preachers again, they dont understand philosophy really well and they try impose
                Ancient Indian teaching on us in a very bad manner(JK)!', '1'
            ), (
                '3', '1', 'The content of the book is fascinating but the only problem which I face is the bent on the edge of the book.
                You can go ahead with this book, one another issue which I face is that pages quality are not upto the mark. This is
                one of the best book for overthinkers.', '4'
            ), (
                '3', '5', 'The quality of the pages is not good. The marks for the words of the other page can be seen on the current one.', '3'
            ), (
                '3', '6', 'Nice book', '5'
            )
        """

        create_status = await self.connection.execute(add_book_data)
        self.check_status(create_status, cfg.DatabaseTables.BOOKS)

        create_status = await self.connection.execute(add_review_data)
        self.check_status(create_status, cfg.DatabaseTables.REVIEWS)

    async def run(self) -> None:
        """ module entrypoint """
        self.connection = await apg.connect(
            user=self.user, password=self.password, database=self.database, host=self.host
        )
        if self.connection is not None:
            await self.create_tables()
            await self.create_data()
        else:
            lg.error("Could not connect to database")
