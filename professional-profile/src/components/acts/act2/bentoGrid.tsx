import SkillCard from "./skillCard";

// Definimos el objeto interno que viene dentro de items conforme al backend
interface SkillItem {
  id: number;
  name: string;
  category: string;
  icon_svg_path: string;
  proficiency_level: number;
}

interface SkillBlock {
  // Ajustado a los nombres exactos de tu SkillBlockOut de Pydantic
  block_title: string;
  category: "data" | "fullstack" | "governance"; 
  icon_name: string; // Token de icono (mapeado desde tu endpoint)
  items: SkillItem[]; // <-- Cambiado de string[] a SkillItem[]
}

async function getSkills(): Promise<SkillBlock[]> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/skills`, {
    next: { revalidate: 3600 } 
  });
  if (!res.ok) throw new Error("Failed to fetch skills");
  return res.json();
}

export default async function BentoGrid() {
  const skillsData = await getSkills();

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 auto-rows-fr">
      {skillsData.map((block, idx) => (
        <SkillCard 
          // Como SkillBlockOut no tiene un campo id directo en tu Pydantic, usamos block_title o idx como key
          key={block.block_title || idx} 
          title={block.block_title}
          items={block.items || []}
          type={block.category}
          iconName={block.icon_name}
          index={idx}
        />
      ))}
    </div>
  );
}