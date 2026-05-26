import data from "@/app/data/proyectos.json";
import { IProject } from "@/models/proyectos";

// 1. Garantizamos la inmutabilidad y el cumplimiento del contrato IProject
const projects: readonly IProject[] = data as unknown as IProject[];


export async function getProjectById(id: string): Promise<IProject | null> {
  const targetId = id.trim();
  
  
  const foundProject = projects.find((p: IProject) => p.id === targetId);
  
  return foundProject ?? null;
}


export async function getAllProjects(): Promise<IProject[]> {
  return [...projects]; 
}