import { useState, useEffect } from 'react';
import { List, Card, Button, Input, message } from 'antd';
const { TextArea } = Input;

interface Post {
    id: number;
    content: string;
    owner_id: number;
    created_at: string;
    likes: any[];
    comments: any[];
}

const Feed = () => {
    const [posts, setPosts] = useState<Post[]>([]);
    const [newPost, setNewPost] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchFeed = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch('http://localhost:8000/posts/', {
                    headers: { Authorization: `Bearer ${token}` },
                });
                if (response.ok) {
                    const data = await response.json();
                    setPosts(data);
                } else {
                    message.error('Failed to load feed');
                }
            } catch (error) {
                message.error('Error loading feed');
            } finally {
                setLoading(false);
            }
        };
        fetchFeed();
    }, []);

    const createPost = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:8000/posts/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
                body: JSON.stringify({ content: newPost }),
            });
            if (response.ok) {
                const added = await response.json();
                setPosts([added, ...posts]);
                setNewPost('');
                message.success('Post created');
            } else {
                message.error('Create failed');
            }
        } catch (error) {
            message.error('Error creating post');
        }
    };

    if (loading) return <div>Loading feed...</div>;

    return (
        <div style={{ maxWidth: 800, margin: 'auto', padding: 20 }}>
            <TextArea
                value={newPost}
                onChange={(e) => setNewPost(e.target.value)}
                placeholder="What's on your mind?"
                rows={4}
            />
            <Button type="primary" onClick={createPost} style={{ marginTop: 10 }}>
                Post
            </Button>
            <List
                itemLayout="vertical"
                dataSource={posts}
                renderItem={(post) => (
                    <List.Item>
                        <Card>
                            <p>{post.content}</p>
                            <p>Posted at: {post.created_at}</p>
                            {/* Add likes/comments here */}
                        </Card>
                    </List.Item>
                )}
            />
        </div>
    );
};

export default Feed;