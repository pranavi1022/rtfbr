import { FloatingPaths } from "@/components/ui/background-paths";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Link } from "react-router-dom";

const Register = () => {
    return (
        <div className="relative min-h-screen w-full flex items-center justify-center overflow-hidden bg-black">
            <div className="absolute inset-0 bg-black" />
            <div className="absolute inset-0">
                <FloatingPaths position={1} />
                <FloatingPaths position={-1} />
            </div>

            <div className="relative z-10 container mx-auto px-4 md:px-6 text-center">
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 2 }}
                    className="max-w-md mx-auto"
                >
                    <h1 className="text-2xl sm:text-3xl font-bold mb-8 tracking-tighter">
                        <motion.span
                            initial={{ y: 100, opacity: 0 }}
                            animate={{ y: 0, opacity: 1 }}
                            transition={{ type: "spring", stiffness: 150, damping: 25 }}
                            className="inline-block text-transparent bg-clip-text bg-gradient-to-r from-white to-white/70"
                        >
                            Create Account
                        </motion.span>
                    </h1>

                    <div className="inline-block group relative bg-gradient-to-b from-white/10 to-white/5 p-px rounded-2xl backdrop-blur-lg overflow-hidden shadow-[0_0_40px_rgba(120,80,255,0.08)]">
                        <div className="rounded-[1.15rem] px-8 py-8 backdrop-blur-md bg-white/[0.05] border border-white/10">
                            <form className="space-y-4 text-left">
                                <div className="space-y-2">
                                    <Label htmlFor="fullname" className="text-white/90">Full Name</Label>
                                    <Input id="fullname" name="fullname" type="text" placeholder="Enter your full name" required className="bg-white/[0.04] border-white/10 text-white placeholder:text-white/30 focus-visible:ring-primary/50 focus-visible:border-primary/40" />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="email" className="text-white/90">Email</Label>
                                    <Input id="email" name="email" type="email" placeholder="Enter your email" required className="bg-white/[0.04] border-white/10 text-white placeholder:text-white/30 focus-visible:ring-primary/50 focus-visible:border-primary/40" />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="username" className="text-white/90">Username</Label>
                                    <Input id="username" name="username" type="text" placeholder="Choose a username" required className="bg-white/[0.04] border-white/10 text-white placeholder:text-white/30 focus-visible:ring-primary/50 focus-visible:border-primary/40" />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="password" className="text-white/90">Password</Label>
                                    <Input id="password" name="password" type="password" placeholder="Create a password" required className="bg-white/[0.04] border-white/10 text-white placeholder:text-white/30 focus-visible:ring-primary/50 focus-visible:border-primary/40" />
                                </div>
                                <Button type="submit" className="w-full bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90 text-primary-foreground font-semibold shadow-[0_0_20px_rgba(120,80,255,0.3)]">
                                    Register
                                </Button>
                                <div className="text-center pt-2">
                                    <Link to="/login" className="text-sm text-white/40 hover:text-white/80 hover:drop-shadow-[0_0_8px_rgba(255,255,255,0.3)] transition-all">
                                        Already have an account? Login
                                    </Link>
                                </div>
                            </form>
                        </div>
                    </div>
                </motion.div>
            </div>
        </div>
    );
};

export default Register;
