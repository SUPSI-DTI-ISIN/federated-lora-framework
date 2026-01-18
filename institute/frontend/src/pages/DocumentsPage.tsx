import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, FileText, Search } from 'lucide-react';
import { DocumentUpload } from '../components/documents/DocumentUpload';
import { DocumentList } from '../components/documents/DocumentList';

export const DocumentsPage = () => {
    const { t } = useTranslation();
    const [searchQuery, setSearchQuery] = useState('');
    const [showUpload, setShowUpload] = useState(false);

    return (
        <div className="min-h-screen bg-linear-to-br from-base-100 via-base-200 to-base-100 py-8 px-4">
            <div className="max-w-7xl mx-auto">
                {/* Page Header */}
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mb-8"
                >
                    <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                        <div>
                            <h1 className="text-4xl font-bold mb-2 flex items-center gap-3">
                                <FileText className="text-primary" size={36} />
                                {t('documents.title')}
                            </h1>
                            <p className="text-base-content/70">
                                {t('documents.subtitle')}
                            </p>
                        </div>
                        <button
                            onClick={() => setShowUpload(true)}
                            className="btn btn-primary gap-2"
                        >
                            <Upload size={20} />
                            {t('documents.uploadButton')}
                        </button>
                    </div>
                </motion.div>

                {/* Search and Filter Bar */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="card bg-base-100 shadow-lg mb-6"
                >
                    <div className="card-body">
                        <div className="flex flex-col md:flex-row gap-4">
                            {/* Search */}
                            <div className="form-control flex-1">
                                <div className="input-group">
                                    <span className="bg-base-200">
                                        <Search size={20} />
                                    </span>
                                    <input
                                        type="text"
                                        placeholder={t('documents.search.placeholder')}
                                        className="input input-bordered w-full"
                                        value={searchQuery}
                                        onChange={(e) => setSearchQuery(e.target.value)}
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                </motion.div>

                {/* Documents List */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                >
                    <DocumentList searchQuery={searchQuery} />
                </motion.div>
            </div>

            {/* Upload Modal */}
            <AnimatePresence>
                {showUpload && (
                    <DocumentUpload onClose={() => setShowUpload(false)} />
                )}
            </AnimatePresence>
        </div>
    );
};