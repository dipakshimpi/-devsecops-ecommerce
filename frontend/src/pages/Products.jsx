import { useState, useEffect } from "react";
import API from "@/api/axios";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ShoppingCart, Package, Loader2, AlertCircle } from "lucide-react";
import { toast } from "sonner";

const Products = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const { data } = await API.get("/products");
        setProducts(data);
      } catch (err) {
        console.error("Error fetching products:", err);
        setError("Could not load products. Please check if the backend is running.");
        toast.error("Error", {
          description: "Failed to load products from the server.",
        });
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
        <Loader2 className="h-10 w-10 animate-spin text-primary" />
        <p className="text-muted-foreground animate-pulse">Loading amazing products...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4 text-center">
        <div className="bg-destructive/10 p-4 rounded-full">
          <AlertCircle className="h-10 w-10 text-destructive" />
        </div>
        <h2 className="text-2xl font-bold">Oops!</h2>
        <p className="text-muted-foreground max-w-md">{error}</p>
        <Button onClick={() => window.location.reload()}>Try Again</Button>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-700">
      <div className="flex flex-col gap-2">
        <h1 className="text-4xl font-extrabold tracking-tight">Our Products</h1>
        <p className="text-muted-foreground">High-quality gear for DevOps engineers and developers.</p>
      </div>

      {products.length === 0 ? (
        <div className="text-center py-20 border rounded-xl bg-muted/30">
          <Package className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
          <h3 className="text-xl font-medium">No products found</h3>
          <p className="text-muted-foreground">Check back later or seed your database!</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {products.map((product) => (
            <Card key={product.id} className="overflow-hidden flex flex-col group hover:shadow-lg transition-all duration-300 border-primary/10">
              <div className="aspect-square bg-muted relative overflow-hidden">
                <img 
                  src={product.image_url || "https://via.placeholder.com/300"} 
                  alt={product.name}
                  className="object-cover w-full h-full group-hover:scale-105 transition-transform duration-500"
                />
                <div className="absolute top-2 right-2 bg-background/80 backdrop-blur-md px-2 py-1 rounded text-xs font-bold border">
                  ${product.price}
                </div>
              </div>
              <CardHeader className="p-4 space-y-1">
                <CardTitle className="text-lg line-clamp-1 group-hover:text-primary transition-colors">
                  {product.name}
                </CardTitle>
              </CardHeader>
              <CardContent className="p-4 pt-0 flex-1">
                <p className="text-sm text-muted-foreground line-clamp-2">
                  {product.description || "No description available."}
                </p>
              </CardContent>
              <CardFooter className="p-4 pt-0">
                <Button className="w-full gap-2 group/btn" variant="secondary">
                  <ShoppingCart className="h-4 w-4 group-hover/btn:translate-x-0.5 transition-transform" />
                  Add to Cart
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default Products;
