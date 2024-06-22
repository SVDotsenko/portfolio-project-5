/**
 * This script is used to validate JavaScript files in the current directory using the CI-JSHint API.
 * It reads the API key from a .env file, iterates over all .js files in the directory, and sends each file to the API
 * for validation.
 * The results are then logged to the console.
 * To run this script locally, you should create a .env file in the same directory where this file is, with the
 * following content: API_KEY=YOUR_API_KEY
 */

const fs = require('fs'); // Node.js File System module for file I/O operations
const path = require('path'); // Node.js Path module for handling and transforming file paths

// Read the .env file and extract the API key
const envPath = path.join(__dirname, '.env');
const envData = fs.readFileSync(envPath, 'utf8');
const API_KEY = envData.split('=')[1]

// Read the current directory
fs.readdir(__dirname, (err, files) => {
    if (err) {
        console.error(err); // Log any error that occurs
        return;
    }

    // Iterate over each file in the directory
    files.forEach(file => {
        // If the file is a JavaScript file and not the current file
        if (path.extname(file) === '.js' && path.resolve(__dirname, file) !== __filename) {
            // Read the file
            fs.readFile(path.join(__dirname, file), 'utf8', (err, data) => {
                if (err) {
                    console.error(err); // Log any error that occurs
                    return;
                }

                // Import the fetch function from the node-fetch module
                import('node-fetch').then((nodeFetch) => {
                    const fetch = nodeFetch.default;

                    // Import the FormData class from the form-data module
                    import('form-data').then((formData) => {
                        const FormData = formData.default;

                        // Create a new form and append the file data and options
                        const form = new FormData();
                        form.append('code', data);
                        form.append('filename', file);
                        form.append('options', 'es6');

                        // Send a POST request to the CI-JSHint API
                        fetch("https://ci-jshint.herokuapp.com/api", {
                            method: "POST",
                            headers: {
                                "Authorization": API_KEY,
                            },
                            body: form,
                        })
                            .then(response => response.json()) // Parse the response as JSON
                            .then(data => {
                                // Log the validation results
                                console.log(`Validation results for ${file}:`, data);
                            })
                            .catch(err => {
                                // Log any error that occurs
                                console.error(err);
                            });
                    });
                });
            });
        }
    });
});