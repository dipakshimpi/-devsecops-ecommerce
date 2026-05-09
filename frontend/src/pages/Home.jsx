import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { ArrowRight, ShoppingBag, ShieldCheck, Zap } from "lucide-react";

const Home = () => {
  return (
    <div className="flex flex-col items-center gap-16 py-12">
      <section className="text-center space-y-6 max-w-3xl">
        <h1 className="text-5xl md:text-6xl font-extrabold tracking-tighter bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent">
          The Ultimate DevOps E-commerce Store
        </h1>
        <p className="text-xl text-muted-foreground">
          Built with React, Node.js, and best-in-class DevOps practices. 
          Ready for Docker, Kubernetes, and AWS deployment.
        </p>
        <div className="flex flex-wrap justify-center gap-4">
          <Link to="/products">
            <Button size="lg" className="gap-2">
              Browse Products <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
          <Link to="/register">
            <Button size="lg" variant="outline">
              Join the Community
            </Button>
          </Link>
        </div>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full">
        <div className="bg-card p-8 rounded-xl border space-y-4">
          <div className="bg-primary/10 w-12 h-12 flex items-center justify-center rounded-lg">
            <Zap className="text-primary h-6 w-6" />
          </div>
          <h3 className="text-xl font-bold">Fast Delivery</h3>
          <p className="text-muted-foreground">Lightning fast shipping for all your DevOps merchandise needs.</p>
        </div>
        <div className="bg-card p-8 rounded-xl border space-y-4">
          <div className="bg-primary/10 w-12 h-12 flex items-center justify-center rounded-lg">
            <ShieldCheck className="text-primary h-6 w-6" />
          </div>
          <h3 className="text-xl font-bold">Secure Auth</h3>
          <p className="text-muted-foreground">Production-grade JWT authentication and secure backend infrastructure.</p>
        </div>
        <div className="bg-card p-8 rounded-xl border space-y-4">
          <div className="bg-primary/10 w-12 h-12 flex items-center justify-center rounded-lg">
            <ShoppingBag className="text-primary h-6 w-6" />
          </div>
          <h3 className="text-xl font-bold">Best Products</h3>
          <p className="text-muted-foreground">Curated selection of quality gear for software engineers and SREs.</p>
        </div>
      </section>
    </div>
  );
};

export default Home;
