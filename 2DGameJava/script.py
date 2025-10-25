
# Create the Java platformer game with rotating rectangle player
# The game will have the player as a rectangle that rotates on its faces to move

# Main game class
main_game = """
import javax.swing.*;
import java.awt.*;

public class RotatingPlatformer {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame("Rotating Rectangle Platformer");
            GamePanel gamePanel = new GamePanel();
            
            frame.add(gamePanel);
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setResizable(false);
            frame.pack();
            frame.setLocationRelativeTo(null);
            frame.setVisible(true);
            
            gamePanel.startGame();
        });
    }
}
"""

# Game panel class with game loop
game_panel = """
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;

public class GamePanel extends JPanel implements Runnable {
    // Screen settings
    private static final int SCREEN_WIDTH = 800;
    private static final int SCREEN_HEIGHT = 600;
    private static final int FPS = 60;
    
    // Game thread
    private Thread gameThread;
    private boolean running = false;
    
    // Game objects
    private Player player;
    private ArrayList<Platform> platforms;
    private KeyHandler keyHandler;
    
    public GamePanel() {
        this.setPreferredSize(new Dimension(SCREEN_WIDTH, SCREEN_HEIGHT));
        this.setBackground(new Color(135, 206, 235)); // Sky blue
        this.setDoubleBuffered(true);
        this.setFocusable(true);
        
        keyHandler = new KeyHandler();
        this.addKeyListener(keyHandler);
        
        initGame();
    }
    
    private void initGame() {
        // Create player at starting position
        player = new Player(100, 300, keyHandler);
        
        // Create platforms
        platforms = new ArrayList<>();
        platforms.add(new Platform(0, 500, 800, 100)); // Ground
        platforms.add(new Platform(200, 400, 200, 30));
        platforms.add(new Platform(450, 300, 150, 30));
        platforms.add(new Platform(650, 200, 150, 30));
        platforms.add(new Platform(300, 150, 200, 30));
    }
    
    public void startGame() {
        running = true;
        gameThread = new Thread(this);
        gameThread.start();
    }
    
    @Override
    public void run() {
        double timePerFrame = 1000000000.0 / FPS;
        long lastTime = System.nanoTime();
        long currentTime;
        double deltaTime;
        
        while (running) {
            currentTime = System.nanoTime();
            deltaTime = (currentTime - lastTime) / timePerFrame;
            lastTime = currentTime;
            
            update(deltaTime);
            repaint();
            
            try {
                Thread.sleep(1000 / FPS);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
    
    private void update(double deltaTime) {
        player.update(deltaTime, platforms);
    }
    
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        
        // Enable anti-aliasing
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        
        // Draw platforms
        for (Platform platform : platforms) {
            platform.draw(g2d);
        }
        
        // Draw player
        player.draw(g2d);
        
        // Draw instructions
        g2d.setColor(Color.BLACK);
        g2d.setFont(new Font("Arial", Font.BOLD, 16));
        g2d.drawString("Arrow Keys to Rotate and Move", 10, 30);
        g2d.drawString("R to Reset", 10, 50);
        
        g2d.dispose();
    }
}
"""

# Player class with rotating rectangle
player_class = """
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
"""

# Platform class
platform_class = """
import java.awt.*;

public class Platform {
    private int x, y, width, height;
    
    public Platform(int x, int y, int width, int height) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }
    
    public Rectangle getBounds() {
        return new Rectangle(x, y, width, height);
    }
    
    public void draw(Graphics2D g2d) {
        // Draw platform
        g2d.setColor(new Color(101, 67, 33)); // Brown
        g2d.fillRect(x, y, width, height);
        
        // Draw border
        g2d.setColor(new Color(80, 50, 20));
        g2d.setStroke(new BasicStroke(2));
        g2d.drawRect(x, y, width, height);
        
        // Draw grass on top
        g2d.setColor(new Color(34, 139, 34));
        g2d.fillRect(x, y, width, 8);
    }
}
"""

# KeyHandler class
key_handler = """
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

public class KeyHandler extends KeyAdapter {
    public boolean leftPressed = false;
    public boolean rightPressed = false;
    public boolean rPressed = false;
    
    @Override
    public void keyPressed(KeyEvent e) {
        int code = e.getKeyCode();
        
        if (code == KeyEvent.VK_LEFT) {
            leftPressed = true;
        }
        if (code == KeyEvent.VK_RIGHT) {
            rightPressed = true;
        }
        if (code == KeyEvent.VK_R) {
            rPressed = true;
        }
    }
    
    @Override
    public void keyReleased(KeyEvent e) {
        int code = e.getKeyCode();
        
        if (code == KeyEvent.VK_LEFT) {
            leftPressed = false;
        }
        if (code == KeyEvent.VK_RIGHT) {
            rightPressed = false;
        }
        if (code == KeyEvent.VK_R) {
            rPressed = false;
        }
    }
}
"""

# Save all files
files = {
    'RotatingPlatformer.java': main_game,
    'GamePanel.java': game_panel,
    'Player.java': player_class,
    'Platform.java': platform_class,
    'KeyHandler.java': key_handler
}

# Write files
for filename, content in files.items():
    with open(filename, 'w') as f:
        f.write(content)

print("Java platformer game files created successfully!")
print("\nFiles created:")
for filename in files.keys():
    print(f"  - {filename}")
print("\n=== HOW TO COMPILE AND RUN ===")
print("1. Open terminal/command prompt in the directory with these files")
print("2. Compile: javac RotatingPlatformer.java GamePanel.java Player.java Platform.java KeyHandler.java")
print("3. Run: java RotatingPlatformer")
print("\n=== GAME CONTROLS ===")
print("- LEFT ARROW: Rotate and move left")
print("- RIGHT ARROW: Rotate and move right")
print("- R: Reset to starting position")
