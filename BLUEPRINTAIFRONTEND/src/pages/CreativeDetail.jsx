import { Link, useParams } from "react-router-dom";

const demoCreatives = [
  {
    id: "1",
    title: "TTAD1 - Smart Water Bottle Creative",
    product: "Smart Water Bottle",
    creator: "Demo Creator 1",
    videoUrl: "/demo-videos/TTAD1.mp4",
    hook: "3-second demo",
    creatorType: "sample collaboration",
    humor: "No humor tag",
    delivery: "No delivery tag",
    score: 8,
    views: "680,891",
    likes: "33,450",
    shares: "1,464",
    clicks: "25,452",
    orders: "2,790",
    insight: "Demo TikTok creative for Smart Water Bottle",
  },
  {
    id: "2",
    title: "TTAD2 - LashLift Kit Creative",
    product: "LashLift Kit",
    creator: "Demo Creator 2",
    videoUrl: "/demo-videos/TTAD2.mp4",
    hook: "shock fact",
    creatorType: "open collaboration",
    humor: "No humor tag",
    delivery: "No delivery tag",
    score: 7,
    views: "591,364",
    likes: "23,103",
    shares: "4,099",
    clicks: "24,281",
    orders: "2,393",
    insight: "Demo TikTok creative for LashLift Kit",
  },
  {
    id: "3",
    title: "TTAD3 - TikTok Product Demo",
    product: "Demo Product",
    creator: "Demo Creator 3",
    videoUrl: "/demo-videos/TTAD3.mp4",
    hook: "visual hook",
    creatorType: "affiliate creator",
    humor: "light humor",
    delivery: "fast-paced demo",
    score: 9,
    views: "720,000",
    likes: "41,000",
    shares: "5,200",
    clicks: "31,000",
    orders: "3,400",
    insight: "High-performing TikTok product demo creative",
  },
  {
    id: "4",
    title: "TTAD4 - Short TikTok Ad",
    product: "Demo Product",
    creator: "Demo Creator 4",
    videoUrl: "/demo-videos/TTAD4.mp4",
    hook: "fast intro",
    creatorType: "organic creator",
    humor: "No humor tag",
    delivery: "short direct pitch",
    score: 6,
    views: "120,000",
    likes: "8,500",
    shares: "640",
    clicks: "6,100",
    orders: "430",
    insight: "Short TikTok-style creative with a simple direct hook",
  },
];

export default function CreativeDetail() {
  const { id } = useParams();
  const creative = demoCreatives.find((item) => item.id === id);

  if (!creative) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold">Creative not found</h1>
        <Link to="/creative-library" className="text-blue-600 hover:underline">
          Back to Creative Library
        </Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 p-8">
      <div className="mx-auto max-w-5xl">
        <Link to="/creative-library" className="mb-6 inline-block text-blue-600 hover:underline">
          ← Back to Creative Library
        </Link>

        <div className="rounded-2xl border bg-white p-6 shadow-sm">
          <h1 className="text-4xl font-bold text-slate-900">{creative.title}</h1>
          <p className="mt-2 text-slate-600">
            {creative.product} · {creative.creator}
          </p>

          <video
            src={creative.videoUrl}
            controls
            className="mt-6 max-h-[600px] w-full rounded-xl border bg-black object-contain"
          />

          <div className="mt-6 flex flex-wrap gap-2">
            <span className="rounded-full border px-3 py-1 text-sm">{creative.hook}</span>
            <span className="rounded-full border px-3 py-1 text-sm">{creative.creatorType}</span>
            <span className="rounded-full border px-3 py-1 text-sm">{creative.humor}</span>
            <span className="rounded-full border px-3 py-1 text-sm">{creative.delivery}</span>
          </div>

          <div className="mt-6 grid grid-cols-2 gap-3 md:grid-cols-6">
            <Metric label="Score" value={creative.score} />
            <Metric label="Views" value={creative.views} />
            <Metric label="Likes" value={creative.likes} />
            <Metric label="Shares" value={creative.shares} />
            <Metric label="Clicks" value={creative.clicks} />
            <Metric label="Orders" value={creative.orders} />
          </div>

          <div className="mt-6 rounded-xl border bg-slate-50 p-5">
            <h2 className="text-xl font-bold text-slate-900">Creative Insight</h2>
            <p className="mt-2 text-slate-700">{creative.insight}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

function Metric({ label, value }) {
  return (
    <div className="rounded-xl border bg-white p-3">
      <p className="text-sm text-slate-500">{label}</p>
      <p className="text-lg font-semibold text-slate-900">{value}</p>
    </div>
  );
}
