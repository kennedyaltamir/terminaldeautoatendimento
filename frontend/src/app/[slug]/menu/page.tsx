import { Suspense } from "react";
import MenuClient from "./MenuClient";
import MenuSkeleton from "@/components/menu/MenuSkeleton";

export default function Page({ params }: { params: { slug: string } }) {
  const { slug } = params; 
  
  return (
    <Suspense fallback={<MenuSkeleton />}>
      <MenuClient slug={slug} />
    </Suspense>
  );
}
