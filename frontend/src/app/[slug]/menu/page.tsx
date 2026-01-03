import MenuClient from "./MenuClient";

export default function Page({ params }: { params: { slug: string } }) {
  const { slug } = params; // Acesso direto (Next.js 14)
  return (
    <MenuClient slug={slug} />
  );
}