// Common helper functions for PostBook application

// GraphQL query function
export const queryGraphQL = async (query, variables = {}) => {
    try {
        const response = await fetch('/graphql', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                variables: variables
            })
        });

        const result = await response.json();
        console.log('GraphQL response:', result);
        return result;
    } catch (error) {
        console.error('GraphQL query error:', error);
        throw error;
    }
};

// Alert display function
export const showAlert = (message, type = 'danger') => {
    const alertContainer = document.getElementById('alert-container');
    if (alertContainer) {
        alertContainer.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
    }
};

// Loading state management for buttons
export const setButtonLoading = (buttonId, textId, spinnerId, loading, loadingText = 'Loading...') => {
    const button = document.getElementById(buttonId);
    const text = document.getElementById(textId);
    const spinner = document.getElementById(spinnerId);

    if (button && text && spinner) {
        if (loading) {
            button.disabled = true;
            if (loadingText !== text.textContent) {
                text.textContent = loadingText;
            }
            spinner.classList.remove('d-none');
        } else {
            button.disabled = false;
            spinner.classList.add('d-none');
        }
    }
};

// Get current user from session
export const getCurrentUser = async () => {
    try {
        const response = await fetch('/api/current-user', {
            credentials: 'include'
        });
        if (response.ok) {
            const userData = await response.json();
            return userData;
        } else {
            throw new Error('Failed to get current user');
        }
    } catch (error) {
        console.error('Error getting current user:', error);
        window.location.href = '/login';
        return null;
    }
};

// Post navigation
export const navigateToPost = (postId) => {
    window.location.href = `/post?post_id=${postId}`;
};

// URL parameter extraction
export const getUrlParameter = (name) => {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
};

// Common GraphQL queries
export const GraphQLQueries = {
    // Fetch all posts
    getAllPosts: async () => {
        const query = `
            {
                getAllPosts {
                    author {
                        name
                    }
                    content
                    id
                    title
                }
            }
        `;
        try {
            const result = await queryGraphQL(query);
            return result.data.getAllPosts || [];
        } catch (error) {
            console.error('Error fetching posts:', error);
            return [];
        }
    },

    // Fetch single post
    getPost: async (postId) => {
        const query = `
            query GetPost($id: Int!) {
                getPost(PostId: $id) {
                    id
                    title
                    content
                    author {
                        name
                    }
                }
            }
        `;
        try {
            const result = await queryGraphQL(query, { id: parseInt(postId) });
            return result.data.getPost;
        } catch (error) {
            console.error('Error fetching post:', error);
            return null;
        }
    },

    // Fetch user's posts
    getUsersPosts: async (userId) => {
        const query = `
            query GetUsersPosts($userId: Int!) {
                getUsersPosts(UserId: $userId) {
                    id
                    title
                    content
                    author {
                        id
                        name
                    }
                }
            }
        `;
        try {
            const result = await queryGraphQL(query, { userId: userId });
            if (result.errors) {
                throw new Error(result.errors[0].message);
            }
            return result.data.getUsersPosts || [];
        } catch (error) {
            console.error('Error fetching user posts:', error);
            throw error;
        }
    },

    // Create post mutation
    createPost: async (title, content, authorId, sessionToken) => {
        const mutation = `
            mutation CreatePost($title: String!, $content: String!, $authorId: Int!, $sessionToken: String!) {
                createPost(title: $title, content: $content, authorId: $authorId, sessionToken: $sessionToken) {
                    id
                    title
                    content
                    author {
                        id
                        name
                    }
                }
            }
        `;
        try {
            const result = await queryGraphQL(mutation, {
                title: title,
                content: content,
                authorId: authorId,
                sessionToken: sessionToken
            });

            if (result.errors) {
                throw new Error(result.errors[0].message);
            }

            return result.data.createPost;
        } catch (error) {
            console.error('Error creating post:', error);
            throw error;
        }
    }
};

// Authentication helpers
export const AuthHelpers = {
    login: async (username, password) => {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const result = await response.json();
        return { response, result };
    },

    register: async (username, password, confirmPassword) => {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password,
                confirm_password: confirmPassword
            })
        });

        const result = await response.json();
        return { response, result };
    },

    logout: async () => {
        try {
            const response = await fetch('/logout', {
                method: 'POST',
                credentials: 'include'
            });

            if (response.ok) {
                window.location.href = '/login';
            } else {
                alert('Error logging out');
            }
        } catch (error) {
            console.error('Logout error:', error);
            alert('Error logging out');
        }
    }
};

// Form validation helpers
export const ValidationHelpers = {
    checkPasswordStrength: (password, strengthElementId) => {
        const strengthDiv = document.getElementById(strengthElementId);
        if (!strengthDiv) return;

        if (password.length === 0) {
            strengthDiv.textContent = '';
            return;
        }

        if (password.length < 6) {
            strengthDiv.textContent = 'Password must be at least 6 characters';
            strengthDiv.className = 'password-strength strength-weak';
        } else if (password.length < 10) {
            strengthDiv.textContent = 'Medium strength';
            strengthDiv.className = 'password-strength strength-medium';
        } else {
            strengthDiv.textContent = 'Strong password';
            strengthDiv.className = 'password-strength strength-strong';
        }
    },

    checkPasswordMatch: (passwordId, confirmPasswordId, matchElementId) => {
        const password = document.getElementById(passwordId).value;
        const confirmPassword = document.getElementById(confirmPasswordId).value;
        const matchDiv = document.getElementById(matchElementId);

        if (!matchDiv) return;

        if (confirmPassword.length === 0) {
            matchDiv.textContent = '';
            return;
        }

        if (password === confirmPassword) {
            matchDiv.textContent = 'Passwords match ✓';
            matchDiv.style.color = '#198754';
        } else {
            matchDiv.textContent = 'Passwords do not match';
            matchDiv.style.color = '#dc3545';
        }
    }
};

// DOM utility functions
export const DOMHelpers = {
    hideAllStates: (stateIds) => {
        stateIds.forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.classList.add('d-none');
            }
        });
    },

    showState: (stateId) => {
        const element = document.getElementById(stateId);
        if (element) {
            element.classList.remove('d-none');
        }
    },

    updateCharacterCount: (inputId, counterId) => {
        const input = document.getElementById(inputId);
        const counter = document.getElementById(counterId);

        if (input && counter) {
            input.addEventListener('input', (e) => {
                counter.textContent = e.target.value.length;
            });
        }
    }
};