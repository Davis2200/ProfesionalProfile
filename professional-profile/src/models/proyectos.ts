export interface IProjectPhase {
  readonly id: string;
  readonly name: string;
  readonly description: string;
}


export interface IProject {
  id: string;          // Identificador único (ej: "banking-churn") [2]
  title: string;       // Nombre del proyecto [6]
  metric: string;      // Resultado clave (ej: "85% ROC-AUC") [7]
  description: string; // Resumen breve para la tarjeta principal
  tag: string;         // Categoría (ej: "Machine Learning", "NLP") [8]
  
  // Campos específicos para el Caso de Estudio
  problem: string;     // El desafío de negocio que resolviste [9]
  process: string;     // Metodología y limpieza de datos aplicada
  tools: string[];     // Tecnologías (ej: ["Python", "XGBoost"]) [10]
  results: string;
  methodology: string; // Metodología científica utilizada
  link: string;  
  docUrl?: string;    // URL al proyecto o repositorio (opcional)
  phases?: readonly IProjectPhase[];
}



