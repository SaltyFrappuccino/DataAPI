import React from "react";

// Узел типа "field"
export const FieldNode = ({ data }) => (
  <div style={{ padding: "10px", border: "1px solid #007aff", borderRadius: "5px", background: "#eaf4ff" }}>
    <strong>Field:</strong> {data.label}
  </div>
);

// Узел типа "operation"
export const OperationNode = ({ data }) => (
  <div style={{ padding: "10px", border: "1px solid #ffa500", borderRadius: "5px", background: "#fff4e6" }}>
    <strong>Operation:</strong> {data.label}
  </div>
);
