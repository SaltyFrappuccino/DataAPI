node_source_responses = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "Успех": {
                        "summary": "Пример успешного запроса",
                        "value": {
                            "id": "123",
                            "data_source_type": "data_source",
                            "connection_type": "SQL",
                            "subtype": "PostgreSQL",
                            "host": "localhost",
                            "port": 5432,
                            "database": "example_db",
                            "file_path": None,
                            "credentials": {"username": "user", "password": "pass"},
                            "test_connection": True,
                        }
                    },
                }
            }
        }
    }
}
node_model_responses = {
    200: {
        "description": "Успешный запрос",
        "content": {
            "application/json": {
                "examples": {
                    "Успех": {
                        "summary": "Пример успешного ответа",
                        "value": {
                            "id": "123",
                            "base_node_type": "base",
                            "label": "Model Node 1",
                            "inputs": {"input1": ["val1", "val2"]},
                            "outputs": {"output1": ["val3", "val4"]},
                            "model_node_type": "model",
                            "environment": "dev",
                            "model_id": "12345",
                            "auth_token": "secret",
                            "timeout": 30,
                        }
                    },
                }
            }
        }
    }
}
