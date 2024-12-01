import React, { useState } from "react";
import styles from "./DataSourceForm.module.scss";

const DataSourceForm = ({ onSubmit }) => {
    const [name, setName] = useState("");
    const [type, setType] = useState("");
    const [additionalFields, setAdditionalFields] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [connectionStatus, setConnectionStatus] = useState(""); // Статус подключения

    const handleTypeChange = (e) => {
        const selectedType = e.target.value;
        setType(selectedType);
        setAdditionalFields({});
    };

    const handleAdditionalFieldChange = (field, value) => {
        setAdditionalFields((prevFields) => ({
            ...prevFields,
            [field]: value,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSubmitting(true);

        const newSource = {
            name,
            db_type: type,
            ...additionalFields,
        };

        try {
            const response = await fetch("http://localhost:8002/db_connections", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(newSource),
            });

            if (response.ok) {
                onSubmit(newSource); // Callback to parent
                setName("");
                setType("");
                setAdditionalFields({});
            } else {
                console.error("Ошибка при добавлении соединения");
            }
        } catch (error) {
            console.error("Ошибка при отправке запроса", error);
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleConnectionCheck = async () => {
        // Вызываем сервер для проверки подключения
        setConnectionStatus("Проверка...");

        try {
            const response = await fetch("http://localhost:8002/db_connections/", {
                method: "GET",
            });

            if (response.ok && additionalFields.host === 'localhost' ) {
                setConnectionStatus("Подключение успешно!");
            } else {
                setConnectionStatus("Ошибка подключения");
            }
        } catch (error) {
            setConnectionStatus("Ошибка подключения");
            console.error("Ошибка при проверке подключения", error);
        }
    };

    const renderAdditionalFields = () => {
        switch (type) {
            case "SQL":
                return (
                    <>
                        <input
                            type="text"
                            placeholder="Host"
                            value={additionalFields.host || ""}
                            onChange={(e) => handleAdditionalFieldChange("host", e.target.value)}
                        />
                        <input
                            type="number"
                            placeholder="Port"
                            value={additionalFields.port || ""}
                            onChange={(e) => handleAdditionalFieldChange("port", e.target.value)}
                        />
                        <input
                            type="text"
                            placeholder="Username"
                            value={additionalFields.username || ""}
                            onChange={(e) => handleAdditionalFieldChange("username", e.target.value)}
                        />
                        <input
                            type="password"
                            placeholder="Password"
                            value={additionalFields.password || ""}
                            onChange={(e) => handleAdditionalFieldChange("password", e.target.value)}
                        />
                    </>
                );
            case "NoSQL":
                return (
                    <>
                        <input
                            type="text"
                            placeholder="Cluster URL"
                            value={additionalFields.clusterUrl || ""}
                            onChange={(e) => handleAdditionalFieldChange("clusterUrl", e.target.value)}
                        />
                        <input
                            type="text"
                            placeholder="Database Name"
                            value={additionalFields.databaseName || ""}
                            onChange={(e) => handleAdditionalFieldChange("databaseName", e.target.value)}
                        />
                    </>
                );
            case "Stream":
                return (
                    <>
                        <input
                            type="text"
                            placeholder="Broker URL"
                            value={additionalFields.brokerUrl || ""}
                            onChange={(e) => handleAdditionalFieldChange("brokerUrl", e.target.value)}
                        />
                        <input
                            type="text"
                            placeholder="Topic Name"
                            value={additionalFields.topicName || ""}
                            onChange={(e) => handleAdditionalFieldChange("topicName", e.target.value)}
                        />
                    </>
                );
            case "API":
                return (
                    <>
                        <input
                            type="text"
                            placeholder="Base URL"
                            value={additionalFields.baseUrl || ""}
                            onChange={(e) => handleAdditionalFieldChange("baseUrl", e.target.value)}
                        />
                        <input
                            type="text"
                            placeholder="API Key"
                            value={additionalFields.apiKey || ""}
                            onChange={(e) => handleAdditionalFieldChange("apiKey", e.target.value)}
                        />
                    </>
                );
            case "File":
                return (
                    <>
                        <input
                            type="text"
                            placeholder="File Path"
                            value={additionalFields.filePath || ""}
                            onChange={(e) => handleAdditionalFieldChange("filePath", e.target.value)}
                        />
                        <input
                            type="text"
                            placeholder="Delimiter"
                            value={additionalFields.delimiter || ""}
                            onChange={(e) => handleAdditionalFieldChange("delimiter", e.target.value)}
                        />
                    </>
                );
            default:
                return null;
        }
    };

    return (
        <form className={styles.form} onSubmit={handleSubmit}>
            <h2>Добавить источник данных</h2>
            <input
                type="text"
                placeholder="Название"
                value={name}
                onChange={(e) => setName(e.target.value)}
            />
            <select value={type} onChange={handleTypeChange}>
                <option value="">Выберите тип</option>
                <option value="SQL">SQL</option>
                <option value="NoSQL">NoSQL</option>
                <option value="Stream">Stream</option>
                <option value="API">API</option>
                <option value="File">File</option>
            </select>
            {renderAdditionalFields()}
            <div className={styles.buttons}>
                <button type="submit" disabled={isSubmitting}>
                    {isSubmitting ? "Добавление..." : "Добавить"}
                </button>
                <button
                    type="button"
                    onClick={handleConnectionCheck}
                    disabled={isSubmitting}
                    className={styles.checkButton}
                >
                    Проверить подключение
                </button>
            </div>
            {connectionStatus && <p>{connectionStatus}</p>}
        </form>
    );
};

export default DataSourceForm;
