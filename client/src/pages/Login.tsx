import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Form, Input, Button, message } from 'antd';

const Login = () => {
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const onFinish = async (values: { username: string; password: string }) => {
        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/users/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `username=${values.username}&password=${values.password}`,
            });
            if (response.ok) {
                const { access_token } = await response.json();
                localStorage.setItem('token', access_token);  // Store JWT
                message.success('Login successful!');
                navigate('/feed');
            } else {
                message.error('Login failed');
            }
        } catch (error) {
            message.error('Error during login');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: 400, margin: 'auto', padding: 20 }}>
            <Form onFinish={onFinish}>
                <Form.Item name="username" rules={[{ required: true, message: 'Enter username' }]}>
                    <Input placeholder="Username" />
                </Form.Item>
                <Form.Item name="password" rules={[{ required: true, message: 'Enter password' }]}>
                    <Input.Password placeholder="Password" />
                </Form.Item>
                <Form.Item>
                    <Button type="primary" htmlType="submit" loading={loading} block>
                        Login
                    </Button>
                </Form.Item>
            </Form>
        </div>
    );
};

export default Login;