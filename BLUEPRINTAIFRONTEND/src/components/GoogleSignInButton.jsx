import { useEffect, useRef } from "react";

export default function GoogleSignInButton({ onSuccess }) {
  const buttonRef = useRef(null);

  useEffect(() => {
    const loadGoogleScript = () => {
      return new Promise((resolve) => {
        if (window.google) return resolve();

        const existing = document.querySelector(
          'script[src="https://accounts.google.com/gsi/client"]'
        );

        if (existing) {
          existing.onload = resolve;
          return;
        }

        const script = document.createElement("script");
        script.src = "https://accounts.google.com/gsi/client";
        script.async = true;
        script.defer = true;
        script.onload = resolve;
        document.body.appendChild(script);
      });
    };

    loadGoogleScript().then(() => {
      if (!window.google || !buttonRef.current) return;

      buttonRef.current.innerHTML = "";

      window.google.accounts.id.initialize({
        client_id:
          "499624760783-ihekcs460fds68vph4frho34m9pngv0d.apps.googleusercontent.com",
        callback: (response) => {
          if (onSuccess) onSuccess(response.credential);
        },
      });

      window.google.accounts.id.renderButton(buttonRef.current, {
        theme: "outline",
        size: "large",
        text: "continue_with",
        shape: "rectangular",
        width: 320,
      });
    });
  }, [onSuccess]);

  return <div ref={buttonRef} />;
}