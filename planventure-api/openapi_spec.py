"""
OpenAPI/Swagger specification for PlanVenture API
"""

swagger_spec = {
    "swagger": "2.0",
    "info": {
        "title": "PlanVenture API",
        "description": "A comprehensive travel planning API for managing trips and itineraries",
        "version": "1.0.0",
        "contact": {
            "name": "PlanVenture Support"
        }
    },
    "host": "127.0.0.1:5000",
    "basePath": "/",
    "schemes": ["http", "https"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT token with Bearer prefix"
        }
    },
    "paths": {
        "/health": {
            "get": {
                "summary": "Health Check",
                "description": "Check if the API server is running",
                "operationId": "health_check",
                "responses": {
                    "200": {
                        "description": "Server is healthy",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "status": {"type": "string", "example": "healthy"}
                            }
                        }
                    }
                }
            }
        },
        "/auth/register": {
            "post": {
                "summary": "Register User",
                "description": "Create a new user account",
                "operationId": "register",
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "username": {"type": "string", "example": "john_doe"},
                                "email": {"type": "string", "format": "email", "example": "john@example.com"},
                                "password": {"type": "string", "example": "StrongPass1!"}
                            },
                            "required": ["username", "email", "password"]
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "User created successfully",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string"},
                                "user": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "integer"},
                                        "username": {"type": "string"},
                                        "email": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "400": {"description": "Missing required fields"},
                    "409": {"description": "User already exists"}
                }
            }
        },
        "/auth/login": {
            "post": {
                "summary": "Login User",
                "description": "Authenticate user and get JWT tokens",
                "operationId": "login",
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "username": {"type": "string"},
                                "password": {"type": "string"}
                            },
                            "required": ["username", "password"]
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Login successful",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string"},
                                "access_token": {"type": "string"},
                                "refresh_token": {"type": "string"},
                                "user": {"type": "object"}
                            }
                        }
                    },
                    "401": {"description": "Invalid credentials"}
                }
            }
        },
        "/profile": {
            "get": {
                "summary": "Get User Profile",
                "description": "Get the current user's profile information",
                "operationId": "get_profile",
                "security": [{"Bearer": []}],
                "responses": {
                    "200": {
                        "description": "User profile",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "username": {"type": "string"},
                                "email": {"type": "string"},
                                "created_at": {"type": "string", "format": "date-time"},
                                "updated_at": {"type": "string", "format": "date-time"}
                            }
                        }
                    },
                    "401": {"description": "Unauthorized"},
                    "404": {"description": "User not found"}
                }
            }
        },
        "/trips": {
            "get": {
                "summary": "Get All Trips",
                "description": "Retrieve all trips for the current user",
                "operationId": "get_trips",
                "security": [{"Bearer": []}],
                "responses": {
                    "200": {
                        "description": "List of trips",
                        "schema": {
                            "type": "array",
                            "items": {"type": "object"}
                        }
                    },
                    "401": {"description": "Unauthorized"}
                }
            },
            "post": {
                "summary": "Create Trip",
                "description": "Create a new trip",
                "operationId": "create_trip",
                "security": [{"Bearer": []}],
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "destination": {"type": "string"},
                                "description": {"type": "string"},
                                "start_date": {"type": "string", "format": "date-time"},
                                "end_date": {"type": "string", "format": "date-time"}
                            },
                            "required": ["title", "destination"]
                        }
                    }
                ],
                "responses": {
                    "201": {"description": "Trip created"},
                    "400": {"description": "Missing required fields"},
                    "401": {"description": "Unauthorized"}
                }
            }
        },
        "/trips/{trip_id}": {
            "get": {
                "summary": "Get Trip",
                "description": "Get details of a specific trip",
                "operationId": "get_trip",
                "security": [{"Bearer": []}],
                "parameters": [
                    {
                        "name": "trip_id",
                        "in": "path",
                        "required": True,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {"description": "Trip details"},
                    "401": {"description": "Unauthorized"},
                    "404": {"description": "Trip not found"}
                }
            },
            "put": {
                "summary": "Update Trip",
                "description": "Update a trip",
                "operationId": "update_trip",
                "security": [{"Bearer": []}],
                "parameters": [
                    {
                        "name": "trip_id",
                        "in": "path",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "name": "body",
                        "in": "body",
                        "schema": {"type": "object"}
                    }
                ],
                "responses": {
                    "200": {"description": "Trip updated"},
                    "401": {"description": "Unauthorized"},
                    "404": {"description": "Trip not found"}
                }
            },
            "delete": {
                "summary": "Delete Trip",
                "description": "Delete a trip",
                "operationId": "delete_trip",
                "security": [{"Bearer": []}],
                "parameters": [
                    {
                        "name": "trip_id",
                        "in": "path",
                        "required": True,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {"description": "Trip deleted"},
                    "401": {"description": "Unauthorized"},
                    "404": {"description": "Trip not found"}
                }
            }
        }
    }
}
