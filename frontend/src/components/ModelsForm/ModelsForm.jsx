import React, { useState } from "react";
import styles from "./ModelsForm.module.scss";

const ModelsForm = ({ onSubmit }) => {
    const [name, setName] = useState("");
    const [settings, setSettings] = useState("");
    const [jsonFile, setJsonFile] = useState(null);

    const handleFileUpload = (e) => {
        const file = e.target.files[0];
        const reader = new FileReader();

        reader.onload = () => {
            const parsedData = JSON.parse(reader.result);
            onSubmit(parsedData);
        };

        reader.readAsText(file);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({ id: Date.now(), name, settings, version: "1.0", image: "https://via.placeholder.com/710x295" });
        setName("");
        setSettings("");
    };

    return (
        <form className={styles.form} onSubmit={handleSubmit}>
            <h2>Добавить модель</h2>
            <input
                type="text"
                placeholder="Название модели"
                value={name}
                onChange={(e) => setName(e.target.value)}
            />
            <textarea
                placeholder="Настройки подключения"
                value={settings}
                onChange={(e) => setSettings(e.target.value)}
            />
            <div className={styles.fileInput}>
                <label htmlFor="file">Или загрузите файл .json:</label>
                <input
                    type="file"
                    id="file"
                    accept=".json"
                    onChange={handleFileUpload}
                />
            </div>
            <button type="submit">Добавить</button>
        </form>
    );
};

export default ModelsForm;
