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
