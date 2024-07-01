class RoutersModule:
    def __init__(self, routers):
        self.routers = routers

    def generate_router(self, router_name):
        router = f"""
        const express = require('express');
        const router = express.Router();
        const controller = require('../controllers/{router_name}.controller');

        router
            .get('/', controller.get )
            .get('/:id', controller.getById )
            .post('/', controller.create )
            .put('/:id', controller.update )
            .delete('/:id', controller._delete );

        module.exports = router;
        """
        return router
    
    def generate_index_router(self):
        index_router = """
        const express = require('express');
    
        // IMPORT ROUTERS
        // EXAMPLE: const users = require('./Users.router');
        
        function routerAPI(app) {
        const router = express.Router();
        app.use('/api', router);
        
        // DEFINE YOUR ROUTERS HERE
        // EXAMPLE: router.use('/users', users);
        
}

        module.exports = routerAPI;
        """
        return index_router