import React from "react";
import styles from "./DataTransformation.module.scss";
import { useNavigate } from "react-router-dom";

const DataTransformation = ({ data }) => {
  const { name, model, language } = data;
  const navigate = useNavigate();

  const handleEdit = () => {
    navigate(`/workflow/${data.name}`);
  };

  return (
    <div className={styles.row}>
      <span>{name}</span>
      <span>{model}</span>
      <span>{language}</span>
      <button className={styles.editButton} onClick={handleEdit}>
        Редактировать
      </button>
    </div>
  );
};

export default DataTransformation;
