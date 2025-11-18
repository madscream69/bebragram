import { useState, useEffect } from 'react';
import { Card, Form, Input, Button, message } from 'antd';

interface User {
    id: number;
    email: string;
    username: string;
    bio?: string;
}

const Profile = () => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch('http://localhost:8000/users/me', {
                    headers: { Authorization: `Bearer ${token}` },
                });
                if (response.ok) {
                    const data = await response.json();
                    setUser(data);
                } else {
                    message.error('Failed to load profile');
                }
            } catch (error) {
                message.error('Error loading profile');
            } finally {
                setLoading(false);
            }
        };
        fetchProfile();
    }, []);

    const onUpdate = async (values: { bio?: string }) => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:8000/users/me', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
                body: JSON.stringify(values),
            });
            if (response.ok) {
                const updated = await response.json();
                setUser(updated);
                message.success('Profile updated');
            } else {
                message.error('Update failed');
            }
        } catch (error) {
            message.error('Error updating profile');
        }
    };

    if (loading) return <div>Loading...</div>;
    if (!user) return <div>No profile data</div>;

    return (
        <Card title="Profile" style={{ maxWidth: 600, margin: 'auto' }}>
            <p>Username: {user.username}</p>
            <p>Email: {user.email}</p>
            <Form onFinish={onUpdate} initialValues={{ bio: user.bio }}>
                <Form.Item name="bio">
                    <Input.TextArea placeholder="Bio" />
                </Form.Item>
                <Button type="primary" htmlType="submit">
                    Update Bio
                </Button>
            </Form>
        </Card>
    );
};

export default Profile;