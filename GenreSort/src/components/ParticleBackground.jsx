import React, { useCallback } from "react";
import Particles from "react-tsparticles";
import { loadSlim } from "tsparticles-slim";

const ParticleBackground = () => {
  const particlesInit = useCallback(async (engine) => {
    await loadSlim(engine);
  }, []);

  const particlesLoaded = useCallback(async (container) => {
    console.log("Particles loaded:", container);
  }, []);

  const particleOptions = {
    fpsLimit: 60,
    interactivity: {
      events: {
        onHover: { enable: false },
        onClick: { enable: false },
        resize: true,
      },
    },
    particles: {
      number: { value: 500, density: { enable: true, area: 2000 } }, // more sparse
      color: { value: "#ffffff" },
      shape: { type: "circle" },
      size: { value: { min: 1, max: 3 } }, // tiny stars
      opacity: { value: 0.8, random: { enable: true, minimumValue: 0.4 } },
      move: {
        enable: true,
        speed: 0.2, // slow drift
        direction: "none", // float in random directions
        outModes: { default: "out" },
        random: true,
        straight: false,
      },
      links: {
        enable: false, // no lines
      },
    },
    detectRetina: true,
  };

  return (
    <Particles
      id="tsparticles"
      init={particlesInit}
      loaded={particlesLoaded}
      options={{ ...particleOptions, background: undefined }}
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        zIndex: 0,
      }}
    />
  );
};

export default ParticleBackground;
