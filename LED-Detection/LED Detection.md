**Sample Codes for different approaches:** https://github.com/Fahim519-ui/LED-Detection

**1\. Multispectral Imaging with Cross-Polarization & Regularized Regression**

Zhen Liu,1,2,4 Kaida Xiao,2,3 Michael Pointer,2 and Changjun Li,3 1 Shanghai Publishing and Printing College, China 2 School of Design, University of Leeds, UK 3School of Computer Science and Software Engineering, University of Science and Technology Liaoning, China 4 School of Statistics, Qufu Normal University, China k.xiao@leeds.ac.uk 

**Core Technical Principle:** This method moves beyond simple RGB values by creating a *multispectral* measurement using a standard camera. It achieves this by controlling the illumination spectrum and using computational techniques to extract maximal information from the sensor data.

**Key Analysis:**

* **Cross-Polarization Physics:**  
  * **How it works:** Light reflecting off a specular (shiny) surface like glass becomes partially polarized. By placing a linear polarizer on the light source (e.g., at 0°) and another on the camera lens rotated 90° to it (90°), the system selectively blocks these specular reflections.  
  * **Why it's critical:** Glare obscures the true color and intensity of the underlying LED. Removing it reveals the diffuse reflection from the LED's semiconductor and phosphor materials, allowing for accurate measurement.  
  * **Implementation:** The polarizer on the light must be aligned with its polarization axis. The camera's polarizer must be rotated until the glare is minimized in the live view. This is often done manually during setup.  
* **Multispectral Data Creation:**  
  * **Two Illuminants:** Using two light sources with different correlated color temperatures (CCTs)—e.g., 3500K (warm white) and 6500K (cool white)—provides two different spectral power distributions. An LED's materials will absorb and reflect these spectra differently.  
  * **Feature Vector Formation:** For a single pixel under one light, you have a 3-dimensional vector (R, G, B). Under two lights, this becomes a 6-dimensional vector V \= \[R1, G1, B1, R2, G2, B2\].  
  * **Polynomial Expansion:** To model non-linear relationships between the input lights and the sensor response, the 6D vector is expanded into a higher-dimensional space. A 3rd-order polynomial expansion of V generates all possible products and powers up to the third degree (e.g., R1, R1², R1\*G1, R1²\*B2, R1\*G2\*B2, etc.). This can create over 80 features from the initial 6 values, capturing complex spectral interactions.  
* **Feature Selection with NCA (Neighbourhood Component Analysis):**  
  * **Problem:** An 80+ feature vector is highly susceptible to overfitting, especially with a limited dataset. Many features are redundant or purely noisy.  
  * **NCA Solution:** NCA is a supervised metric learning algorithm. It learns a weight for each feature that maximizes the leave-one-out classification accuracy on the training data. Features with weights near zero are irrelevant for distinguishing between the classes (e.g., "Red On" vs. "Green On").  
  * **Output:** NCA ranks the features. The top *N* most important features (e.g., 30\) are selected for model training, drastically reducing dimensionality and noise.  
* **Regularized Regression (Ridge Regression):**  
  * **Model Task:** The problem is framed as regression to predict continuous intensity values or multivariate regression for (R, G, B) output. Classification can also be used.  
  * **Overfitting Prevention:** Even with selected features, models can overfit. Ridge Regression (L2 regularization) adds a penalty term λ \* ||weights||² to the loss function. This penalty discourages the model from assigning excessively large weights to any feature, forcing it to distribute importance and create a smoother, more generalizable model.  
  * **Equation (Simplified):** Loss \= Σ(y\_true \- y\_pred)² \+ λ \* Σ(weight\_i²). The hyperparameter λ controls the strength of the regularization.

**Pros:** Extremely robust to glare and ambient light; high accuracy for color and intensity; based on sound optical physics.  
**Cons:** Complex setup requiring calibrated lights and polarizers; computationally expensive feature expansion and selection; requires a curated training dataset.

**2\. VLC-based Detection using Flicker and CNN**

Guan, W., Li, J., Wen, S., Zhang, X., Ye, Y., Zheng, J., & Jiang, J. (2019). The Detection and Recognition of RGB-LED-ID Based on Visible Light Communication using Convolutional Neural Network. *Applied Sciences*, *9*(7), 1400\. https://doi.org/10.3390/app9071400

**Core Technical Principle:** This method treats the LED not as a static light source but as a data transmitter. It leverages the rolling shutter mechanism of standard CMOS cameras to capture high-frequency flicker patterns that are imperceptible to the human eye.

**Key Analysis:**

* **Modulation Schemes (PWM, OFDM, OFC):**  
  * **PWM (Pulse Width Modulation):** The LED is switched on and off at a fixed frequency. The duty cycle ( percentage of "on" time) controls perceived brightness. The *frequency* itself can be used as an ID.  
  * **OFC (Optical Fringe Code):** A more advanced communication scheme where data is encoded in the width and spacing of the light and dark "fringes" (stripes) captured by the camera.  
  * **Purpose:** This flicker encodes information—a unique device ID, a status code, or sensor data—directly from the LED.  
* **Rolling Shutter Effect:**  
  * **Mechanism:** Unlike global shutter cameras that capture all pixels simultaneously, CMOS sensors in smartphones and many industrial cameras capture pixels row-by-row. This takes time (e.g., 1/30th of a second for a full frame).  
  * **Creating Stripes:** If an LED is flickering faster than the frame rate, its state (on/off) changes *while* the frame is being captured. This results in a picture where the LED appears as a series of dark and bright bands (stripes). The pattern of these stripes is a direct visualization of the LED's flicker over time.  
* **The Blooming Challenge:**  
  * **Cause:** When an LED is too bright, charge from over-saturated pixels spills into adjacent pixels in the sensor column. This creates a vertical "smear" or bloom that obscures the precise horizontal stripe pattern.  
  * **Mitigation:** The ROI for analysis is carefully chosen to avoid the most bloomed central columns of the LED image. Adaptive contrast enhancement and thresholding algorithms are used to try and recover the signal from the bloomed background.  
* **Convolutional Neural Network (CNN) Classifier:**  
  * **Input:** The CNN is not fed raw signal data. Its input is the *image of the striped LED*.  
  * **Architecture:** The CNN's layers (convolutional, pooling) are excellent at learning spatial hierarchies of features. Early layers learn to detect simple edges (the transitions between stripes), while deeper layers learn complex combinations of these edges to recognize the overall pattern (e.g., "three thin bright stripes followed by one wide dark stripe").  
  * **Output:** The final layer classifies this pattern into a predefined category (e.g., "LED ID \#5" or "Message: OK").

**Pros:** Enables unique identification and data transmission from LEDs; uses inexpensive CMOS sensors; has high potential accuracy for trained patterns.  
**Cons:** Requires LEDs to be specially modulated; highly susceptible to blooming which ruins data; performance depends on camera frame rate and shutter speed; requires significant training data for the CNN.

**3\. Active Synchronized Hyperspectral Illumination**

**Core Technical Principle:** This is the most powerful and complex method. It constructs a hyperspectral image cube (x, y, λ) by actively illuminating the scene with narrowband light sources (LEDs at specific wavelengths) and synchronizing the camera capture with each source.  
**In-Depth Analysis:**

* **Hyperspectral Data Cube:** A three-dimensional dataset where each pixel (x, y) has a full spectrum of intensities across many wavelengths (λ), providing a unique spectral signature.  
* **LED Array Design:**  
  * **Narrowband LEDs:** The system uses LEDs with very narrow emission spectra (e.g., 5nm FWHM \- Full Width at Half Maximum). Each LED acts as a discrete monochromatic light source (e.g., 365nm, 450nm, 520nm, 630nm, 850nm, 940nm).  
  * **Uniform Illumination:** The LEDs are arranged in concentric rings to ensure the target is evenly illuminated from all angles, minimizing shadows and specular highlights.  
* **Synchronization:**  
  * A microcontroller (e.g., Arduino, FPGA) sequentially turns on each LED in the array.  
  * For each LED illuminated, it triggers the camera to take a picture.  
  * The result is a stack of images, each showing the object under a very specific wavelength of light. This stack is the hyperspectral cube.  
* **Spectral Calibration:** The intensity values in each image are normalized using a reference card (e.g., white, grey) placed in the scene to account for the varying power output of each LED and sensor sensitivity at different wavelengths.  
* **Machine Learning Application:** The hypercube is used to train classifiers like Random Forests or CNNs. The model learns to identify materials or states based on their reflectance spectrum, which is a much more powerful descriptor than simple RGB.

**Pros:** Provides immense discriminative power; can identify materials, chemicals, and states far beyond human vision; gold standard for precision.  
**Cons:** Extreme overkill for simple LED state detection; very slow data acquisition (seconds per object); extremely complex and expensive hardware; massive data processing requirements.

**4\. Light Identification using HSV Color Space**

Xiaoqiang Wang et al, 2018 J. Phys.: Conf. Ser. 1074 012081

**Core Technical Principle:** This is a simple, efficient image processing technique that relies on the decomposition of color into channels that are more aligned with human perception: Hue (color type), Saturation (color purity), and Value (brightness).  
**In-Depth Analysis:**

* **Color Space Transformation:**  
  * **Why HSV:** RGB values are highly correlated and sensitive to changes in illumination intensity. HSV decouples this information.  
  * **Hue (H):** Represents the dominant wavelength. A red LED and a dim red LED will have a similar Hue. This makes color recognition robust to slight intensity changes.  
  * **Saturation (S):** Represents the purity of the color. A vivid red has high saturation; a faded pink has low saturation. This helps distinguish a bright LED from a dim one or a reflection.  
  * **Value (V):** Represents the lightness or intensity. This is the primary indicator for On/Off state.  
* **Thresholding:**  
  * **Process:** For each predefined LED ROI, the average H, S, and V values are computed.  
  * **Rule-Based Classification:**  
    * **On/Off:** IF V \< threshold THEN OFF ELSE ON  
    * **Color:** IF ON AND (H\_low\_red \< H \< H\_high\_red) AND S \> saturation\_min THEN RED  
      IF ON AND (H\_low\_green \< H \< H\_high\_green) THEN GREEN  
  * **Calibration:** The threshold values (H\_low\_red, saturation\_min, etc.) must be determined empirically for the specific camera, lens, and lighting environment.

**Pros:** Extreme simplicity and computational efficiency; very easy to implement and debug; no special hardware required.  
**Cons:** **Extremely fragile.** Fails with any glare, significant ambient light changes, auto-white-balance, or if the LED color does not perfectly fall within the predefined thresholds. Lacks any robustness for industrial environments.

