"use client";
import { useState, useEffect, useRef } from "react";
import { ArrowRight, Link, Zap } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BorderRotate } from "@/components/ui/animated-gradient-border";

interface TimelineItem {
  id: number;
  title: string;
  date: string;
  content: string;
  category: string;
  icon: React.ElementType;
  relatedIds: number[];
  status: "completed" | "in-progress" | "pending";
  energy: number;
  link?: string;
}

interface RadialOrbitalTimelineProps {
  timelineData: TimelineItem[];
}

export type { TimelineItem, RadialOrbitalTimelineProps };

export default function RadialOrbitalTimeline({
  timelineData,
}: RadialOrbitalTimelineProps) {
  const [expandedItems, setExpandedItems] = useState<Record<number, boolean>>({});
  const [viewMode] = useState<"orbital">("orbital");
  const [rotationAngle, setRotationAngle] = useState<number>(0);
  const [autoRotate, setAutoRotate] = useState<boolean>(true);
  const [pulseEffect, setPulseEffect] = useState<Record<number, boolean>>({});
  const [centerOffset] = useState<{ x: number; y: number }>({ x: 0, y: 0 });
  const [activeNodeId, setActiveNodeId] = useState<number | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const orbitRef = useRef<HTMLDivElement>(null);
  const nodeRefs = useRef<Record<number, HTMLDivElement | null>>({});

  const handleContainerClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === containerRef.current || e.target === orbitRef.current) {
      setExpandedItems({});
      setActiveNodeId(null);
      setPulseEffect({});
      setAutoRotate(true);
    }
  };

  const toggleItem = (id: number) => {
    setExpandedItems((prev) => {
      const newState = { ...prev };
      Object.keys(newState).forEach((key) => {
        if (parseInt(key) !== id) {
          newState[parseInt(key)] = false;
        }
      });
      newState[id] = !prev[id];

      if (!prev[id]) {
        setActiveNodeId(id);
        setAutoRotate(false);
        const relatedItems = getRelatedItems(id);
        const newPulseEffect: Record<number, boolean> = {};
        relatedItems.forEach((relId) => {
          newPulseEffect[relId] = true;
        });
        setPulseEffect(newPulseEffect);
        centerViewOnNode(id);
      } else {
        setActiveNodeId(null);
        setAutoRotate(true);
        setPulseEffect({});
      }
      return newState;
    });
  };

  useEffect(() => {
    let rotationTimer: ReturnType<typeof setInterval>;
    if (autoRotate && viewMode === "orbital") {
      rotationTimer = setInterval(() => {
        setRotationAngle((prev) => {
          const newAngle = (prev + 0.3) % 360;
          return Number(newAngle.toFixed(3));
        });
      }, 50);
    }
    return () => {
      if (rotationTimer) clearInterval(rotationTimer);
    };
  }, [autoRotate, viewMode]);

  const centerViewOnNode = (nodeId: number) => {
    if (viewMode !== "orbital" || !nodeRefs.current[nodeId]) return;
    const nodeIndex = timelineData.findIndex((item) => item.id === nodeId);
    const totalNodes = timelineData.length;
    const targetAngle = (nodeIndex / totalNodes) * 360;
    setRotationAngle(270 - targetAngle);
  };

  const calculateNodePosition = (index: number, total: number) => {
    const angle = ((index / total) * 360 + rotationAngle) % 360;
    const radius = 180;
    const radian = (angle * Math.PI) / 180;
    const x = radius * Math.cos(radian) + centerOffset.x;
    const y = radius * Math.sin(radian) + centerOffset.y;
    const zIndex = Math.round(100 + 50 * Math.cos(radian));
    const opacity = Math.max(0.4, Math.min(1, 0.4 + 0.6 * ((1 + Math.sin(radian)) / 2)));
    return { x, y, angle, zIndex, opacity };
  };

  const getRelatedItems = (itemId: number): number[] => {
    const currentItem = timelineData.find((item) => item.id === itemId);
    return currentItem ? currentItem.relatedIds : [];
  };

  const isRelatedToActive = (itemId: number): boolean => {
    if (!activeNodeId) return false;
    const relatedItems = getRelatedItems(activeNodeId);
    return relatedItems.includes(itemId);
  };

  const getStatusStyles = (status: TimelineItem["status"]): string => {
    switch (status) {
      case "completed":
        return "text-white bg-black border-white";
      case "in-progress":
        return "text-black bg-white border-black";
      case "pending":
        return "text-white bg-black/40 border-white/50";
      default:
        return "text-white bg-black/40 border-white/50";
    }
  };

  /* silver / mercury gradient for BorderRotate */
  const silverGradient = {
    primary: '#4a4a4a',
    secondary: '#a0a0a0',
    accent: '#e0e0e0',
  };

  return (
    <div
      className="w-full flex flex-col items-center justify-center overflow-hidden"
      style={{ height: "500px" }}
      ref={containerRef}
      onClick={handleContainerClick}
    >
      <div className="relative w-full max-w-4xl h-full flex items-center justify-center">
        <div
          className="absolute w-full h-full flex items-center justify-center"
          ref={orbitRef}
          style={{
            perspective: "1000px",
            transform: `translate(${centerOffset.x}px, ${centerOffset.y}px)`,
          }}
        >
          {/* center core – enhanced glow */}
          <div className="absolute w-16 h-16 rounded-full bg-gradient-to-br from-white/30 via-white/15 to-white/5 animate-pulse flex items-center justify-center z-10">
            <div className="absolute w-20 h-20 rounded-full border-2 border-white/30 animate-ping opacity-70"></div>
            <div
              className="absolute w-24 h-24 rounded-full border border-white/20 animate-ping opacity-50"
              style={{ animationDelay: "0.5s" }}
            ></div>
            <div className="absolute w-28 h-28 rounded-full border border-white/10 opacity-30" style={{ boxShadow: '0 0 40px rgba(255,255,255,0.15)' }}></div>
            <div className="w-8 h-8 rounded-full bg-white/90 backdrop-blur-md shadow-[0_0_20px_rgba(255,255,255,0.6)]"></div>
          </div>

          {/* orbit ring – enhanced */}
          <div
            className="absolute w-96 h-96 rounded-full border-2 border-white/[0.15]"
            style={{ boxShadow: '0 0 30px rgba(255,255,255,0.06), inset 0 0 30px rgba(255,255,255,0.04)' }}
          ></div>

          {timelineData.map((item, index) => {
            const position = calculateNodePosition(index, timelineData.length);
            const isExpanded = expandedItems[item.id];
            const isRelated = isRelatedToActive(item.id);
            const isPulsing = pulseEffect[item.id];
            const Icon = item.icon;
            const stepNumber = index + 1;

            const nodeStyle = {
              transform: `translate(${position.x}px, ${position.y}px)`,
              zIndex: isExpanded ? 200 : position.zIndex,
              opacity: isExpanded ? 1 : position.opacity,
            };

            return (
              <div
                key={item.id}
                ref={(el) => (nodeRefs.current[item.id] = el)}
                className="absolute transition-all duration-700 cursor-pointer"
                style={nodeStyle}
                onClick={(e) => {
                  e.stopPropagation();
                  toggleItem(item.id);
                }}
              >
                {/* energy glow */}
                <div
                  className={`absolute rounded-full -inset-1 ${isPulsing ? "animate-pulse duration-1000" : ""}`}
                  style={{
                    background: `radial-gradient(circle, rgba(255,255,255,0.25) 0%, rgba(255,255,255,0) 70%)`,
                    width: `${item.energy * 0.5 + 40}px`,
                    height: `${item.energy * 0.5 + 40}px`,
                    left: `-${(item.energy * 0.5 + 40 - 40) / 2}px`,
                    top: `-${(item.energy * 0.5 + 40 - 40) / 2}px`,
                  }}
                ></div>

                {/* step number badge – positioned above node */}
                <div
                  className={`absolute -top-5 left-1/2 -translate-x-1/2 w-5 h-5 rounded-full flex items-center justify-center text-[9px] font-bold z-10
                    ${isExpanded
                      ? "bg-white text-black shadow-[0_0_12px_rgba(255,255,255,0.6)]"
                      : "bg-white/20 text-white/80 border border-white/30"
                    } transition-all duration-300`}
                >
                  {stepNumber}
                </div>

                {/* node circle – enhanced glow */}
                <div
                  className={`
                  w-10 h-10 rounded-full flex items-center justify-center
                  ${isExpanded ? "bg-white text-black" : isRelated ? "bg-white/50 text-black" : "bg-black text-white"}
                  border-2 
                  ${isExpanded
                    ? "border-white shadow-[0_0_20px_rgba(255,255,255,0.5),0_0_40px_rgba(255,255,255,0.2)]"
                    : isRelated
                    ? "border-white animate-pulse shadow-[0_0_15px_rgba(255,255,255,0.3)]"
                    : "border-white/50 shadow-[0_0_10px_rgba(255,255,255,0.15)]"}
                  transition-all duration-300 transform
                  ${isExpanded ? "scale-150" : "hover:scale-110"}
                `}
                >
                  <Icon size={16} />
                </div>

                {/* label */}
                <div
                  className={`
                  absolute top-12 whitespace-nowrap
                  text-xs font-semibold tracking-wider
                  transition-all duration-300
                  ${isExpanded ? "text-white scale-125" : "text-white/70"}
                `}
                >
                  {item.title}
                </div>

                {/* expanded card – wrapped with BorderRotate silver */}
                {isExpanded && (
                  <div className="absolute top-20 left-1/2 -translate-x-1/2">
                    <BorderRotate
                      animationMode="auto-rotate"
                      animationSpeed={4}
                      gradientColors={silverGradient}
                      backgroundColor="#0a0a0a"
                      borderWidth={2}
                      borderRadius={12}
                      className="w-72"
                    >
                      <Card className="w-full bg-black/90 backdrop-blur-lg border-0 shadow-xl shadow-white/10 overflow-visible rounded-none">
                        <div className="absolute -top-3 left-1/2 -translate-x-1/2 w-px h-3 bg-white/50"></div>
                        <CardHeader className="pb-2">
                          <div className="flex justify-between items-center">
                            <Badge className={`px-2 text-xs ${getStatusStyles(item.status)}`}>
                              {item.status === "completed" ? "COMPLETE" : item.status === "in-progress" ? "IN PROGRESS" : "PENDING"}
                            </Badge>
                            <span className="text-xs font-mono text-white/50">{item.date}</span>
                          </div>
                          <CardTitle className="text-sm mt-2 text-white">{item.title}</CardTitle>
                        </CardHeader>
                        <CardContent className="text-xs text-white/80">
                          <p>{item.content}</p>

                          <div className="mt-4 pt-3 border-t border-white/10">
                            <div className="flex justify-between items-center text-xs mb-1">
                              <span className="flex items-center">
                                <Zap size={10} className="mr-1" />
                                Importance
                              </span>
                              <span className="font-mono">{item.energy}%</span>
                            </div>
                            <div className="w-full h-1 bg-white/10 rounded-full overflow-hidden">
                              <div
                                className="h-full bg-gradient-to-r from-white/40 to-white/80"
                                style={{ width: `${item.energy}%` }}
                              ></div>
                            </div>
                          </div>

                          {item.link && (
                            <a
                              href={item.link}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="mt-3 inline-flex items-center gap-1 text-xs text-white/60 hover:text-white transition-colors underline underline-offset-4"
                              onClick={(e) => e.stopPropagation()}
                            >
                              Start learning →
                            </a>
                          )}

                          {item.relatedIds.length > 0 && (
                            <div className="mt-4 pt-3 border-t border-white/10">
                              <div className="flex items-center mb-2">
                                <Link size={10} className="text-white/70 mr-1" />
                                <h4 className="text-xs uppercase tracking-wider font-medium text-white/70">Connected</h4>
                              </div>
                              <div className="flex flex-wrap gap-1">
                                {item.relatedIds.map((relatedId) => {
                                  const relatedItem = timelineData.find((i) => i.id === relatedId);
                                  return (
                                    <Button
                                      key={relatedId}
                                      variant="outline"
                                      size="sm"
                                      className="flex items-center h-6 px-2 py-0 text-xs rounded-none border-white/20 bg-transparent hover:bg-white/10 text-white/80 hover:text-white transition-all"
                                      onClick={(e) => {
                                        e.stopPropagation();
                                        toggleItem(relatedId);
                                      }}
                                    >
                                      {relatedItem?.title}
                                      <ArrowRight size={8} className="ml-1 text-white/60" />
                                    </Button>
                                  );
                                })}
                              </div>
                            </div>
                          )}
                        </CardContent>
                      </Card>
                    </BorderRotate>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
