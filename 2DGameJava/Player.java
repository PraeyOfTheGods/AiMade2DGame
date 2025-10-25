
import java.awt.*;
import java.awt.geom.*;
import java.util.ArrayList;

public class Player {
    // Player dimensions
    private static final int WIDTH = 50;
    private static final int HEIGHT = 80;

    // Physics
    private double x, y;
    private double velocityX = 0;
    private double velocityY = 0;
    private double gravity = 0.6;
    private double rotationAngle = 0;

    // Rotation animation
    private boolean isRotating = false;
    private double targetRotation = 0;
    private double rotationSpeed = 8.0;
    private int rotationDirection = 0; // -1 left, 1 right

    // Movement
    private boolean onGround = false;
    private KeyHandler keyHandler;

    // Starting position for reset
    private double startX, startY;

    public Player(double x, double y, KeyHandler keyHandler) {
        this.x = x;
        this.y = y;
        this.startX = x;
        this.startY = y;
        this.keyHandler = keyHandler;
    }

    public void update(double deltaTime, ArrayList<Platform> platforms) {
        // Handle reset
        if (keyHandler.rPressed) {
            reset();
        }

        // Handle rotation input (only when on ground and not already rotating)
        if (onGround && !isRotating) {
            if (keyHandler.leftPressed) {
                startRotation(-1);
            } else if (keyHandler.rightPressed) {
                startRotation(1);
            }
        }

        // Update rotation animation
        if (isRotating) {
            updateRotation();
        }

        // Apply gravity
        velocityY += gravity;

        // Update position
        y += velocityY;
        x += velocityX;

        // Check collisions with platforms
        onGround = false;
        Rectangle playerBounds = getBounds();

        for (Platform platform : platforms) {
            if (playerBounds.intersects(platform.getBounds())) {
                Rectangle platformBounds = platform.getBounds();

                // Vertical collision
                if (velocityY > 0) { // Falling down
                    y = platformBounds.y - HEIGHT;
                    velocityY = 0;
                    onGround = true;
                } else if (velocityY < 0) { // Moving up
                    y = platformBounds.y + platformBounds.height;
                    velocityY = 0;
                }

                // Horizontal collision
                if (velocityX > 0) { // Moving right
                    x = platformBounds.x - WIDTH;
                    velocityX = 0;
                    isRotating = false;
                } else if (velocityX < 0) { // Moving left
                    x = platformBounds.x + platformBounds.width;
                    velocityX = 0;
                    isRotating = false;
                }
            }
        }

        // Stop horizontal movement when rotation is complete
        if (!isRotating && Math.abs(velocityX) > 0) {
            velocityX *= 0.85; // Friction
            if (Math.abs(velocityX) < 0.1) {
                velocityX = 0;
            }
        }

        // Keep player on screen
        if (x < 0) x = 0;
        if (x > 800 - WIDTH) x = 800 - WIDTH;

        // Fall off screen detection
        if (y > 650) {
            reset();
        }
    }

    private void startRotation(int direction) {
        isRotating = true;
        rotationDirection = direction;
        targetRotation = rotationAngle + (Math.PI / 2) * direction;

        // Calculate horizontal movement distance
        double moveDistance = (WIDTH + HEIGHT) / 2.0;
        velocityX = moveDistance / (Math.PI / 2 / rotationSpeed) * direction;
    }

    private void updateRotation() {
        double diff = targetRotation - rotationAngle;

        if (Math.abs(diff) > 0.05) {
            rotationAngle += rotationSpeed * Math.signum(diff) * Math.PI / 180;
        } else {
            rotationAngle = targetRotation;
            isRotating = false;
            velocityX = 0;
        }
    }

    private void reset() {
        x = startX;
        y = startY;
        velocityX = 0;
        velocityY = 0;
        rotationAngle = 0;
        isRotating = false;
    }

    public Rectangle getBounds() {
        return new Rectangle((int)x, (int)y, WIDTH, HEIGHT);
    }

    public void draw(Graphics2D g2d) {
        // Save original transform
        AffineTransform originalTransform = g2d.getTransform();

        // Calculate center point for rotation
        double centerX = x + WIDTH / 2.0;
        double centerY = y + HEIGHT / 2.0;

        // Apply rotation
        g2d.rotate(rotationAngle, centerX, centerY);

        // Draw the rectangle
        g2d.setColor(new Color(255, 80, 80));
        g2d.fillRect((int)x, (int)y, WIDTH, HEIGHT);

        // Draw border
        g2d.setColor(new Color(200, 50, 50));
        g2d.setStroke(new BasicStroke(3));
        g2d.drawRect((int)x, (int)y, WIDTH, HEIGHT);

        // Draw a line to show orientation
        g2d.setColor(Color.WHITE);
        g2d.setStroke(new BasicStroke(2));
        g2d.drawLine((int)centerX, (int)y, (int)centerX, (int)(y + HEIGHT/3));

        // Restore original transform
        g2d.setTransform(originalTransform);
    }
}
