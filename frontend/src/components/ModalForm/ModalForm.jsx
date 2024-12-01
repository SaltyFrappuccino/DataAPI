import React from "react";
import styles from "./ModalForm.module.scss";

const ModalForm = ({ isOpen, onClose, children }) => {
    if (!isOpen) return null;

    return (
        <div className={styles.modalOverlay} onClick={onClose}>
            <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
                {children}
                {/*<button className={styles.closeButton} onClick={onClose}>*/}
                {/*    Закрыть*/}
                {/*</button>*/}
            </div>
        </div>
    );
};

export default ModalForm;
