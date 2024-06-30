class DBConfigModule:
    def __init__(self):
        pass
    
    def generate_sequelize_config(self):
        sequelize = """
        const { Sequelize } = require('sequelize');
        const  { config } = require('../config/config');
        const setupModels = require('./../models');

        const sequelize = new Sequelize(
            config.dbName, // NAME DATABASE
            config.dbUser, // USER DATABASE
            config.dbPassword, // PASSWORD DATABASE
            {
            host: config.dbHost,
            dialect: 'mysql' // TYPE DATABASE
            }
        );

        sequelize.sync();
        setupModels(sequelize);

        module.exports = sequelize;
        """
        return sequelize

    def generate_config(self):
        config = """
        require('dotenv').config();

        const config = {
        env: process.env.NODE_ENV || 'DEFAULT', // CHANGE DEFAULT TO YOUR ENVIRONMENT
        port: process.env.DB_PORT || 3000, // PORT
        dbUser:  process.env.DB_USER,
        dbPassword:  process.env.DB_PASSWORD,
        dbHost:  process.env.DB_HOST,
        dbName:  process.env.DB_NAME,
        dbPort:  process.env.DB_PORT,
        }

        module.exports = { config };
        """
        return config
    
    def generate_env(self):
        env = """
        NODE_ENV=DEFAULT
        DB_USER=root
        DB_PASSWORD=
        DB_HOST=localhost
        DB_NAME=database
        DB_PORT=3306
        """
        return env
    
    def generate_index(self):
        index = """
        const express = require('express');
        const dotenv = require('dotenv');
        const cors = require('cors');
        const bodyParser = require('body-parser');

        dotenv.config();
        const app = express();
        const APIRouter = require('./routes');
        const PORT = process.env.PORT || 3000;

        // MIDLEWARES
        const corsOptions = {
        origin: '*', // ALLOW ALL ORIGIN
        methods: 'GET,HEAD,PUT,PATCH,POST,DELETE', // HTTP METHODS ALLOWED
        allowedHeaders: 'Content-Type,Authorization', // HEADERS ALLOWED
        credentials: true, // COOKIES ALLOWED
        };

        app.use(cors(corsOptions));
        app.use(express.json({ limit: '10mb' }));
        app.use(express.urlencoded({ extended: true, limit: '10mb' }));
        app.use(bodyParser.json({ limit: '10mb' }));
        app.use(bodyParser.urlencoded({ extended: true, limit: '10mb' }));

        // ROUTES - CHANGE TO YOUR ROUTES
        app.get('/api', (req, res) => {
        res.send('API is running!');
        });

        APIRouter(app);

        app.listen(PORT, () => {
        console.log(`SERVER RUNNING ON PORT ${PORT}`);
        });
        """
        return index