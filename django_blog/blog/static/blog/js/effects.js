// Particle network animation
document.addEventListener('DOMContentLoaded', function() {
  // Create particle network
  createParticleNetwork();
 
  // Add scroll animations
  initScrollAnimations();
 
  // Add interactive effects
  initInteractiveEffects();
});
 
function createParticleNetwork() {
  const canvas = document.createElement('canvas');
  canvas.classList.add('particle-network');
  document.body.appendChild(canvas);
 
  const ctx = canvas.getContext('2d');
  let particles = [];
  const particleCount = 100;
 
  function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
 
  window.addEventListener('resize', resizeCanvas);
  resizeCanvas();
 
  // Create particles
  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      size: Math.random() * 2 + 1,
      speedX: Math.random() * 0.5 - 0.25,
      speedY: Math.random() * 0.5 - 0.25,
      color: `rgba(99, 102, 241, ${Math.random() * 0.2 + 0.1})`
    });
  }
 
  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
 
    // Update and draw particles
    particles.forEach(particle => {
      particle.x += particle.speedX;
      particle.y += particle.speedY;
 
      // Wrap around edges
      if (particle.x > canvas.width) particle.x = 0;
      if (particle.x < 0) particle.x = canvas.width;
      if (particle.y > canvas.height) particle.y = 0;
      if (particle.y < 0) particle.y = canvas.height;
 
      // Draw particle
      ctx.beginPath();
      ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
      ctx.fillStyle = particle.color;
      ctx.fill();
    });
 
    // Draw connections
    particles.forEach((particle, i) => {
      particles.slice(i).forEach(otherParticle => {
        const dx = particle.x - otherParticle.x;
        const dy = particle.y - otherParticle.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
 
        if (distance < 150) {
          ctx.beginPath();
          ctx.strokeStyle = `rgba(99, 102, 241, ${0.2 * (1 - distance / 150)})`;
          ctx.lineWidth = 0.5;
          ctx.moveTo(particle.x, particle.y);
          ctx.lineTo(otherParticle.x, otherParticle.y);
          ctx.stroke();
        }
      });
    });
 
    requestAnimationFrame(animate);
  }
 
  animate();
}
 
function initScrollAnimations() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };
 
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate__animated', 'animate__fadeInUp');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);
 
  // Observe elements with animation class
  document.querySelectorAll('.blog-post.card, .feature-card').forEach(el => {
    observer.observe(el);
  });
}
 
function initInteractiveEffects() {
  // Add ripple effect to buttons
  document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function(e) {
      const x = e.clientX - e.target.getBoundingClientRect().left;
      const y = e.clientY - e.target.getBoundingClientRect().top;
 
      const ripple = document.createElement('span');
      ripple.classList.add('ripple');
      ripple.style.left = `${x}px`;
      ripple.style.top = `${y}px`;
      this.appendChild(ripple);
 
      setTimeout(() => {
        ripple.remove();
      }, 600);
    });
  });
 
  // Add tilt effect to cards
  document.querySelectorAll('.blog-post.card').forEach(card => {
    card.addEventListener('mousemove', function(e) {
      const rect = this.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
 
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
 
      const angleY = (x - centerX) / 25;
      const angleX = (centerY - y) / 25;
 
      this.style.transform = `perspective(1000px) rotateX(${angleX}deg) rotateY(${angleY}deg) translateZ(10px)`;
    });
 
    card.addEventListener('mouseleave', function() {
      this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateZ(0)';
    });
  });
}