interface CardSkeletonProps {
    count: number;
}

export const CardSkeleton = ({count}: CardSkeletonProps) => {
    const items = Array.from({length: count}, (_, i) => i);

    return (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3" role="status" aria-label="Loading content">
            {items.map((i) => (
                <div key={i} className="card bg-base-100 shadow-md">
                    <div className="card-body p-6">
                        <div className="mb-3 h-5 w-3/4 animate-pulse rounded bg-base-300"/>
                        <div className="mb-4 h-6 w-20 animate-pulse rounded-full bg-base-300"/>
                        <div className="space-y-2">
                            <div className="h-3 w-full animate-pulse rounded bg-base-300"/>
                            <div className="h-3 w-5/6 animate-pulse rounded bg-base-300"/>
                        </div>
                        <div className="card-actions mt-4 justify-end gap-2">
                            <div className="h-8 w-16 animate-pulse rounded-lg bg-base-300"/>
                            <div className="h-8 w-16 animate-pulse rounded-lg bg-base-300"/>
                        </div>
                    </div>
                </div>
            ))}
            <span className="sr-only">Loading...</span>
        </div>
    );
}
