import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import "../creative-library.css";
import { getEngineAnalysis, getSelectedShopId } from "../services/engineApi";

const demoCreatives = [
  {
    id: 1,
    title: "TTAD1 - Creator Product Review",
    product: "Demo Product",
    creator: "Demo Creator 1",
    videoUrl: "/demo-videos/TTAD1.mp4",
    hook: "review hook",
    creatorType: "affiliate creator",
    humor: "No humor tag",
    delivery: "testimonial style",
    score: 8,
    views: "680,891",
    likes: "33,450",
    shares: "1,464",
    clicks: "25,452",
    orders: "2,790",
    insight: "A creator-led review style ad that introduces the product through personal experience.",
  },
  {
    id: 2,
    title: "TTAD2 - Beauty Product Demo",
    product: "Beauty Product",
    creator: "Demo Creator 2",
    videoUrl: "/demo-videos/TTAD2.mp4",
    hook: "visual transformation",
    creatorType: "beauty creator",
    humor: "No humor tag",
    delivery: "calm demo",
    score: 7,
    views: "591,364",
    likes: "23,103",
    shares: "4,099",
    clicks: "24,281",
    orders: "2,393",
    insight: "A beauty-focused TikTok ad using close-up visuals and product application.",
  },
  {
    id: 3,
    title: "TTAD3 - Product Close-Up Creative",
    product: "Demo Product",
    creator: "Demo Creator 3",
    videoUrl: "/demo-videos/TTAD3.mp4",
    hook: "close-up product hook",
    creatorType: "product demo creator",
    humor: "No humor tag",
    delivery: "fast-paced demo",
    score: 9,
    views: "720,000",
    likes: "41,000",
    shares: "5,200",
    clicks: "31,000",
    orders: "3,400",
    insight: "Strong product visuals that quickly show what the viewer is supposed to focus on.",
  },
  {
    id: 4,
    title: "TTAD4 - Short Brand Clip",
    product: "Demo Product",
    creator: "Brand Creative",
    videoUrl: "/demo-videos/TTAD4.mp4",
    hook: "brand intro",
    creatorType: "brand-made ad",
    humor: "No humor tag",
    delivery: "short direct pitch",
    score: 6,
    views: "120,000",
    likes: "8,500",
    shares: "640",
    clicks: "6,100",
    orders: "430",
    insight: "A short branded creative that can be used as a simple TikTok Shop product ad.",
  },
  {
    id: 5,
    title: "TTAD5 - Lifestyle Product Use",
    product: "Lifestyle Product",
    creator: "Demo Creator 5",
    videoUrl: "/demo-videos/TTAD5.mp4",
    hook: "day-in-life hook",
    creatorType: "lifestyle creator",
    humor: "No humor tag",
    delivery: "natural use case",
    score: 8,
    views: "502,300",
    likes: "28,900",
    shares: "2,100",
    clicks: "18,430",
    orders: "1,820",
    insight: "Shows the product being used in a natural real-life setting, which helps the ad feel less forced.",
  },
  {
    id: 6,
    title: "TTAD6 - Problem/Solution Ad",
    product: "Demo Product",
    creator: "Demo Creator 6",
    videoUrl: "/demo-videos/TTAD6.mp4",
    hook: "problem-solution hook",
    creatorType: "UGC creator",
    humor: "No humor tag",
    delivery: "explainer style",
    score: 7,
    views: "438,100",
    likes: "19,700",
    shares: "1,850",
    clicks: "14,210",
    orders: "1,240",
    insight: "Uses a problem/solution structure that makes the product benefit easier to understand.",
  },
  {
    id: 7,
    title: "TTAD7 - Phone Audio Mistake Ad",
    product: "Mini Lavalier Mic",
    creator: "Demo Creator 7",
    videoUrl: "/demo-videos/TTAD7.mp4",
    hook: "mistake hook",
    creatorType: "tech creator",
    humor: "light humor",
    delivery: "direct creator pitch",
    score: 9,
    views: "812,500",
    likes: "52,800",
    shares: "6,400",
    clicks: "39,200",
    orders: "4,120",
    insight: "A strong hook-based ad that calls out a common creator mistake and positions the product as the fix.",
  },
  {
    id: 8,
    title: "TTAD8 - Creator Talking Head Ad",
    product: "Demo Product",
    creator: "Demo Creator 8",
    videoUrl: "/demo-videos/TTAD8.mp4",
    hook: "talking-head hook",
    creatorType: "educational creator",
    humor: "No humor tag",
    delivery: "face-to-camera",
    score: 8,
    views: "635,900",
    likes: "36,100",
    shares: "3,700",
    clicks: "22,800",
    orders: "2,610",
    insight: "A face-to-camera TikTok ad that feels like a natural creator recommendation.",
  },
];

export default function CreativeLibrary() {
  const [search, setSearch] = useState("");
  const [engineCreatives, setEngineCreatives] = useState([]);

  useEffect(() => {
    async function loadEngineCreatives() {
      try {
        const data = await getEngineAnalysis(getSelectedShopId());
        const mapped = (data.scored_creatives || []).map((item, index) => ({
          id: item.creative_id || index + 1,
          title: item.title || `Creative ${index + 1}`,
          product: item.title?.replace("Demo TikTok creative for ", "") || "Demo Product",
          creator: item.labels?.creator_type || "TikTok Creator",
          videoUrl: demoCreatives[index % demoCreatives.length]?.videoUrl || "/demo-videos/TTAD1.mp4",
          hook: item.labels?.hook_type || "Unknown hook",
          creatorType: item.labels?.creator_type || "Unknown creator",
          humor: item.labels?.visual_style || "No humor tag",
          delivery: item.labels?.product_angle || "Product angle",
          score: item.score || "—",
          views: item.metrics?.views?.toLocaleString?.() || item.metrics?.views || "0",
          likes: item.metrics?.likes?.toLocaleString?.() || item.metrics?.likes || "0",
          shares: item.metrics?.shares?.toLocaleString?.() || item.metrics?.shares || "0",
          clicks: item.metrics?.clicks?.toLocaleString?.() || item.metrics?.clicks || "0",
          orders: item.metrics?.orders?.toLocaleString?.() || item.metrics?.orders || "0",
          insight: item.performance_status || "Analyzed by BluePrintAI engine.",
        }));

        if (mapped.length) setEngineCreatives(mapped);
      } catch (err) {
        console.warn("Using fallback demo creatives:", err);
      }
    }

    loadEngineCreatives();
  }, []);

  const creatives = engineCreatives.length ? engineCreatives : demoCreatives;

  const filteredCreatives = useMemo(() => {
    const query = search.trim().toLowerCase();

    if (!query) return creatives;

    return creatives.filter((creative) => {
      const searchableText = [
        creative.title,
        creative.product,
        creative.creator,
        creative.hook,
        creative.creatorType,
        creative.humor,
        creative.delivery,
        creative.insight,
      ]
        .join(" ")
        .toLowerCase();

      return searchableText.includes(query);
    });
  }, [search, creatives]);

  return (
    <section className="creative-library-page">
      <div className="creative-library-shell">
        <div className="creative-library-hero">
          <div>
            <p className="creative-eyebrow">Creative Intelligence</p>
            <h1>Creative Library</h1>
            <p>
              Compare hooks, creator types, humor, delivery, and performance across
              your TikTok Shop creatives.
            </p>
          </div>
        </div>

        <div className="creative-filter-card">
          <input
            placeholder="Search creatives..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <select>
            <option>All hook types</option>
          </select>
          <select>
            <option>All creator types</option>
          </select>
        </div>

        <div className="creative-list">
          {filteredCreatives.length === 0 ? (
            <div className="creative-empty-state">
              No creatives found for "{search}".
            </div>
          ) : (
            filteredCreatives.map((creative) => (
            <article key={creative.id} className="creative-card">
              <Link to={`/creatives/${creative.id}`} className="creative-video-wrap">
                <video
                  src={creative.videoUrl}
                  controls
                  playsInline
                  preload="metadata"
                  className="creative-video"
                />
              </Link>

              <div className="creative-card-content">
                <div className="creative-card-top">
                  <div>
                    <Link to={`/creatives/${creative.id}`} className="creative-title">
                      {creative.title}
                    </Link>
                    <p className="creative-meta">
                      {creative.product} · {creative.creator}
                    </p>
                  </div>

                  <div className="creative-score">
                    <span>Score</span>
                    <strong>{creative.score}</strong>
                  </div>
                </div>

                <div className="creative-tags">
                  <span>{creative.hook}</span>
                  <span>{creative.creatorType}</span>
                  <span>{creative.humor}</span>
                  <span>{creative.delivery}</span>
                </div>

                <div className="creative-metrics">
                  <Metric label="Views" value={creative.views} />
                  <Metric label="Likes" value={creative.likes} />
                  <Metric label="Shares" value={creative.shares} />
                  <Metric label="Clicks" value={creative.clicks} />
                  <Metric label="Orders" value={creative.orders} />
                </div>

                <p className="creative-insight">{creative.insight}</p>

                <Link to={`/creatives/${creative.id}`} className="creative-detail-link">
                  View creative details →
                </Link>
              </div>
            </article>
          ))
          )}
        </div>
      </div>
    </section>
  );
}

function Metric({ label, value }) {
  return (
    <div className="creative-metric-card">
      <p>{label}</p>
      <strong>{value}</strong>
    </div>
  );
}
