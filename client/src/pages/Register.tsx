import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Form, Input, Button, message } from 'antd';

const Register = () => {
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const onFinish = async (values: { email: string; username: string; password: string; bio?: string }) => {
        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/users/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(values),
            });
            if (response.ok) {
                message.success('Registration successful! Please log in.');
                navigate('/login');
            } else {
                message.error('Registration failed');
            }
        } catch (error) {
            message.error('Error during registration');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: 400, margin: 'auto', padding: 20 }}>
            <Form onFinish={onFinish}>
                <Form.Item name="email" rules={[{ required: true, type: 'email', message: 'Enter valid email' }]}>
                    <Input placeholder="Email" />
                </Form.Item>
                <Form.Item name="username" rules={[{ required: true, message: 'Enter username' }]}>
                    <Input placeholder="Username" />
                </Form.Item>
                <Form.Item name="password" rules={[{ required: true, message: 'Enter password' }]}>
                    <Input.Password placeholder="Password" />
                </Form.Item>
                <Form.Item name="bio">
                    <Input.TextArea placeholder="Bio (optional)" />
                </Form.Item>
                <Form.Item>
                    <Button type="primary" htmlType="submit" loading={loading} block>
                        Register
                    </Button>
                </Form.Item>
            </Form>
        </div>
    );
};

export default Register;