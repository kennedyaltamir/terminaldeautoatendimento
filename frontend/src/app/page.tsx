import Navbar from "@/components/landing/Navbar";
import Hero from "@/components/landing/Hero";
import Integrations from "@/components/landing/Integrations";
import UseCases from "@/components/landing/UseCases";
import Simulator from "@/components/landing/Simulator";
import Workflow from "@/components/landing/Workflow";
import Features from "@/components/landing/Features";
import RoiCalculator from "@/components/landing/RoiCalculator";
import Testimonials from "@/components/landing/Testimonials";
import FeeComparison from "@/components/landing/FeeComparison";
import Hardware from "@/components/landing/Hardware";
import Comparison from "@/components/landing/Comparison";
import Pricing from "@/components/landing/Pricing";
import TrustBadges from "@/components/landing/TrustBadges";
import FAQ from "@/components/landing/FAQ";
import LeadMagnet from "@/components/landing/LeadMagnet";
import Footer from "@/components/landing/Footer";
import FloatingWidget from "@/components/landing/FloatingWidget";
import CustomCursor from "@/components/ui/CustomCursor";
import BeforeAfter from "@/components/landing/BeforeAfter";
import LiveTicker from "@/components/landing/LiveTicker";
import CookieBanner from "@/components/ui/CookieBanner";
import ScrollReveal from "@/components/ui/ScrollReveal";
import LeadCapture from "@/components/landing/LeadCapture"; // NOVO

export default function LandingPage() {
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "MesaFlow",
    "applicationCategory": "BusinessApplication",
    "operatingSystem": "Web",
    "offers": {
      "@type": "Offer",
      "price": "0",
      "priceCurrency": "BRL"
    },
    "description": "Sistema operacional de autoatendimento para restaurantes e eventos."
  };

  return (
    <div className="min-h-screen bg-white dark:bg-gray-950 selection:bg-orange-100 selection:text-orange-900 font-sans scroll-smooth cursor-none transition-colors duration-300">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      
      <CustomCursor />
      <div className="scroll-progress"></div>
      
      <Navbar />
      
      <main>
        <Hero />
        
        <ScrollReveal>
          <Integrations />
        </ScrollReveal>
        
        <ScrollReveal>
          <Simulator />
        </ScrollReveal>
        
        <ScrollReveal>
          <UseCases />
        </ScrollReveal>
        
        <ScrollReveal>
          <Workflow />
        </ScrollReveal>
        
        <ScrollReveal>
          <BeforeAfter />
        </ScrollReveal>
        
        <ScrollReveal>
          <Features />
        </ScrollReveal>
        
        <ScrollReveal>
          <Testimonials />
        </ScrollReveal>
        
        <ScrollReveal>
          <RoiCalculator />
        </ScrollReveal>
        
        <ScrollReveal>
          <FeeComparison />
        </ScrollReveal>
        
        <ScrollReveal>
          <Hardware />
        </ScrollReveal>
        
        <ScrollReveal>
          <Comparison />
        </ScrollReveal>
        
        <Pricing />
        
        <ScrollReveal>
          <TrustBadges />
        </ScrollReveal>
        
        <ScrollReveal>
          <FAQ />
        </ScrollReveal>
        
        <ScrollReveal>
          <LeadMagnet />
        </ScrollReveal>
      </main>
      
      <Footer />
      <FloatingWidget />
      <LiveTicker />
      <CookieBanner />
      <LeadCapture /> {/* NOVO: Popup de Captura */}
    </div>
  );
}