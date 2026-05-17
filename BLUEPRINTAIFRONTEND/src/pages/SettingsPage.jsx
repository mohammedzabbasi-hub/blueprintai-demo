import {
  User,
  ShoppingBag,
  Film,
  CreditCard,
  LogOut,
  Check,
  ExternalLink,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Link } from "react-router-dom";

export default function SettingsPage() {
  return (
    <div className="max-w-2xl mx-auto space-y-6 animate-fade-in">
      <div className="bg-card rounded-xl border p-6 shadow-card">
        <div className="flex items-center gap-3 mb-6">
          <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center">
            <User className="h-5 w-5 text-primary" />
          </div>
          <div>
            <h2 className="font-semibold">Account Information</h2>
            <p className="text-sm text-muted-foreground">Manage your profile</p>
          </div>
        </div>
        <div className="space-y-4">
          <div>
            <Label>Full Name</Label>
            <Input defaultValue="Alex Johnson" className="mt-1.5" />
          </div>
          <div>
            <Label>Email</Label>
            <Input
              defaultValue="alex@glowbeautyshop.com"
              className="mt-1.5"
            />
          </div>
          <Button className="gradient-primary text-primary-foreground">
            Save Changes
          </Button>
        </div>
      </div>

      <div className="bg-card rounded-xl border p-6 shadow-card">
        <div className="flex items-center gap-3 mb-4">
          <ShoppingBag className="h-5 w-5 text-primary" />
          <h2 className="font-semibold">Connected TikTok Shop</h2>
        </div>
        <div className="rounded-lg border border-success/30 bg-success/5 p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Check className="h-5 w-5 text-success" />
            <div>
              <p className="font-medium text-sm">GlowBeauty Shop</p>
              <p className="text-xs text-muted-foreground">
                Connected on March 1, 2024
              </p>
            </div>
          </div>
          <Button variant="outline" size="sm">
            Disconnect
          </Button>
        </div>
      </div>

      <div className="bg-card rounded-xl border p-6 shadow-card">
        <div className="flex items-center gap-3 mb-4">
          <Film className="h-5 w-5 text-primary" />
          <h2 className="font-semibold">Manage Creatives</h2>
        </div>
        <p className="text-sm text-muted-foreground mb-4">
          You have 24 creatives imported from your TikTok Shop.
        </p>
        <Button variant="outline" asChild>
          <Link to="/creatives">View Creative Library</Link>
        </Button>
      </div>

      <div className="bg-card rounded-xl border p-6 shadow-card">
        <div className="flex items-center gap-3 mb-4">
          <CreditCard className="h-5 w-5 text-primary" />
          <h2 className="font-semibold">Billing</h2>
        </div>
        <p className="text-sm text-muted-foreground mb-2">
          Current Plan: <span className="font-semibold text-foreground">Pro</span>
        </p>
        <p className="text-sm text-muted-foreground mb-4">
          Next billing date: April 1, 2024
        </p>
        <Button variant="outline">Manage Subscription</Button>
      </div>

      <div className="bg-card rounded-xl border p-6 shadow-card">
        <h2 className="font-semibold mb-4">Legal</h2>
        <div className="space-y-2">
          <a
            href="#"
            className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            Privacy Policy <ExternalLink className="h-3 w-3" />
          </a>
          <a
            href="#"
            className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            Terms of Service <ExternalLink className="h-3 w-3" />
          </a>
        </div>
      </div>

      <Button variant="destructive" className="w-full">
        <LogOut className="mr-2 h-4 w-4" /> Log Out
      </Button>
    </div>
  );
}